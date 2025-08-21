import datetime
import os

import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from base.base_function import BaseFunction
from base.instance.config_instance import ConfigInstance


class TrainerFunction(BaseFunction):
    def __init__(self, instance: ConfigInstance):
        super().__init__()
        self.instance = instance

        log_root = os.path.join(self.instance.save_root, 'log')
        os.makedirs(log_root, exist_ok=True)
        self.writer = SummaryWriter(log_root)

    def save(self, step, score, name):
        torch.save({
            'parameters': self.instance.model.state_dict(),
            'step': step,
            'score': score
        }, os.path.join(self.instance.save_root, f'{name}.pth'))

    def batch_train(self, batch):
        batch = list(batch)
        for i, item in enumerate(batch):
            batch[i] = item.to(self.instance.device).float()

        with torch.cuda.amp.autocast():
            out = self.instance.predictor(batch)
            losses = self.instance.criterion([*out, *batch])
        loss = torch.zeros(()).to(self.instance.device)
        for item in losses:
            loss += item
        self.instance.scheduler.zero_grad()
        torch.nn.utils.clip_grad_norm_(self.instance.model.parameters(), 1)
        loss.backward()
        self.instance.scheduler.step()
        return loss.detach().cpu().numpy()

    def batch_predict(self, batch):
        batch = list(batch)
        for i, item in enumerate(batch):
            batch[i] = item.to(self.instance.device).float()
        with torch.cuda.amp.autocast():
            out = self.instance.predictor(batch)
            score = self.instance.metric([out, *batch])
        return score

    def train(self, data_loader, epoch):
        index = (epoch - 1) * len(data_loader)

        bar = tqdm(data_loader)
        for batch in bar:
            loss = self.batch_train(batch)

            if (index + 1) % self.instance.show_step == 0:
                loss_v = str(np.round(loss, decimals=5))
                bar.set_postfix_str(f'index: {(index + 1)}, loss: {loss_v}')
            self.writer.add_scalar('train/loss', loss, global_step=index)
            index = index + 1

    def predict(self, dataloader, epoch):
        self.instance.model.eval()
        scores = []
        with torch.no_grad():
            bar = tqdm(dataloader)
            for j, batch in enumerate(bar):
                score = self.batch_predict(batch)
                scores.append(score)
        scores = np.mean(np.array(scores))
        self.instance.model.train()
        return scores

    def infer(self, *batch):
        batch = list(batch)
        for i, item in enumerate(batch):
            batch[i] = item.to(self.instance.device).float()
        with torch.cuda.amp.autocast():
            sample = self.instance.predictor(batch)
        return sample

    def forward(self, inference_epoch=-1, is_train_valid=False):
        best_score = self.instance.best_score

        train_loader = self.instance.data['train']
        train_data_length = len(train_loader)

        start_epoch = self.instance.start_step // train_data_length
        for i in range(start_epoch + 1, self.instance.epoch + 1):
            print(f'{datetime.datetime.now()}, epoch {i}/{self.instance.epoch}')
            self.train(train_loader, i)

            if i % inference_epoch != 0:
                continue

            if is_train_valid:
                score = self.predict(self.instance.data['train'], i)
                self.writer.add_scalar(f"train/score", score, i)
            score = self.predict(self.instance.data['valid'], i)
            self.writer.add_scalar(f"valid/score", score, i)
            if best_score is None or best_score < score:
                best_score = score
                print(f'{datetime.datetime.now()}, cur best model, score: {best_score}')
                self.save(i * train_data_length, best_score, 'best')
            else:
                print(f'{datetime.datetime.now()}, pre best model, score: {best_score}')
            print(f'{datetime.datetime.now()}, last model, score: {score}')
            self.save(i * train_data_length, score, 'last')
