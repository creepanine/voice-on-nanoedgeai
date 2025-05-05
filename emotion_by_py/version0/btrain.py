import torch
from torch.autograd import Variable 
import utils
from attack_method import *
import torch.nn as nn
import torch.optim as optim
from time import clock
import os
import torch.nn.functional as F


class Adversarial_Trainings(object):
    def __init__(self,  repeat_num , trainloader, use_cuda, attack_iters, net, multi_net, epsilon, alpha, learning_rate_decay_start, learning_rate_decay_every, learning_rate_decay_rate, lr, multi_lr, save_path, gamma1, gamma2):
        self.trainloader = trainloader
        self.repeat_num = repeat_num
        self.use_cuda = use_cuda
        self.attack_iters = attack_iters
        self.net = net
        self.epsilon = epsilon
        self.alpha = alpha
        self.learning_rate_decay_start = learning_rate_decay_start
        self.learning_rate_decay_every = learning_rate_decay_every
        self.learning_rate_decay_rate = learning_rate_decay_rate
        self.lr = lr
        self.save_path = save_path
        self.optimizer = optim.SGD(self.net.parameters(), lr=self.lr, momentum=0.9, weight_decay=5e-4)
        self.multi_net = multi_net
        self.multi_optimizer = optim.SGD(multi_net.parameters(), lr = multi_lr , momentum=0.9, weight_decay=5e-4)
        self.gamma1 = gamma1
        self.gamma2 = gamma2


    def Stardard_Training(self, total_epoch):
        self.net.train()
        for epoch in range(total_epoch):
            print('\nEpoch: %d' % epoch)
            train_loss = 0
            correct = 0
            total = 0
            if epoch > self.learning_rate_decay_start and self.learning_rate_decay_start >= 0:
                frac = (epoch - self.learning_rate_decay_start) // self.learning_rate_decay_every
                decay_factor = self.learning_rate_decay_rate ** frac
                current_lr = self.lr * decay_factor
                utils.set_lr(self.optimizer, current_lr)  # set the decayed rate
            else:
                current_lr = self.lr
            print('learning_rate: %s' % str(current_lr))

            for batch_idx, (inputs, targets) in enumerate(self.trainloader):
                if self.use_cuda:
                    inputs, targets = inputs.cuda(), targets.cuda()
                self.optimizer.zero_grad()
                inputs, targets = Variable(inputs), Variable(targets)
                outputs = self.net(inputs)
                loss = nn.CrossEntropyLoss()(outputs, targets)
                loss.backward()
                utils.clip_gradient(self.optimizer, 0.1)
                self.optimizer.step()

                train_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += predicted.eq(targets.data).cpu().sum()

                utils.progress_bar(batch_idx, len(self.trainloader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
                    % (train_loss/(batch_idx+1), 100.*correct/total, correct, total))
            Train_acc = 100.*correct/total
        torch.save(self.net.state_dict(), 'base_model.pt')
        return self.net


    def pgd_advTraining(self, total_epoch):
        self.net.train()
        for epoch in range(total_epoch):
            print('\nEpoch: %d' % epoch)
            train_loss = 0
            correct = 0
            total = 0
            if epoch > self.learning_rate_decay_start and self.learning_rate_decay_start >= 0:
                frac = (epoch - self.learning_rate_decay_start) // self.learning_rate_decay_every
                decay_factor = self.learning_rate_decay_rate ** frac
                current_lr = self.lr * decay_factor
                utils.set_lr(self.optimizer, current_lr)  # set the decayed rate
            else:
                current_lr = self.lr
            print('learning_rate: %s' % str(current_lr))

            for batch_idx, (inputs, targets) in enumerate(self.trainloader):
                if self.use_cuda:
                    inputs, targets = inputs.cuda(), targets.cuda()
                self.optimizer.zero_grad()
                inputs, targets = Variable(inputs), Variable(targets)

                delta = torch.zeros_like(inputs)

                for repeat_ in range(self.repeat_num):
                    # Generating adversarial examples
                    adversarial_attack = Adversarial_methods(inputs + delta, targets, self.attack_iters, self.net, self.epsilon, self.alpha) 
                    delta = adversarial_attack.fgsm()

                # Update network parameters
                outputs = self.net(torch.clamp(inputs + delta, 0, 1))
                loss = nn.CrossEntropyLoss()(outputs, targets)
                loss.backward()
                utils.clip_gradient(self.optimizer, 0.1)
                self.optimizer.step()

                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += predicted.eq(targets.data).cpu().sum()

                utils.progress_bar(batch_idx, len(self.trainloader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
                    % (train_loss/(batch_idx+1), 100.*correct/total, correct, total))
            Train_acc = 100.*correct/total
            print("The final free_fast accuracy is :", Train_acc)
        torch.save(self.net.state_dict(), 'pgd__base_model.pt')
        return self.net



    def fast_advTraining(self, total_epoch):
        self.net.train()
        for epoch in range(total_epoch):
            print('\nEpoch: %d' % epoch)
            train_loss = 0
            correct = 0
            total = 0

            if epoch > self.learning_rate_decay_start and self.learning_rate_decay_start >= 0:
                frac = (epoch - self.learning_rate_decay_start) // self.learning_rate_decay_every
                decay_factor = self.learning_rate_decay_rate ** frac
                current_lr = self.lr * decay_factor
                utils.set_lr(self.optimizer, current_lr)  # set the decayed rate
            else:
                current_lr = self.lr
            print('learning_rate: %s' % str(current_lr))

            for batch_idx, (inputs, targets) in enumerate(self.trainloader):
                if self.use_cuda:
                    inputs, targets = inputs.cuda(), targets.cuda()
                self.optimizer.zero_grad()
                inputs, targets = Variable(inputs), Variable(targets)


                # Generating adversarial examples
                adversarial_attack = Adversarial_methods(inputs, targets, self.attack_iters, self.net, self.epsilon, self.alpha) 
                delta = adversarial_attack.rfgsm()
                # Update network parameters
                outputs = self.net(torch.clamp(inputs + delta, 0, 1))
                loss = nn.CrossEntropyLoss()(outputs, targets)
                loss.backward()
                utils.clip_gradient(self.optimizer, 0.1)
                self.optimizer.step()

                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += predicted.eq(targets.data).cpu().sum()

                utils.progress_bar(batch_idx, len(self.trainloader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
                    % (train_loss/(batch_idx+1), 100.*correct/total, correct, total))

            Train_acc = 100.*correct/total
        print("The final free_fast accuracy is :", Train_acc)
        torch.save(self.net.state_dict(), 'fast_base_model.pt')
        return self.net

    def free_advTraining(self, total_epoch):
        self.net.train()
        for epoch in range(total_epoch):
            print('\nEpoch: %d' % epoch)
            train_loss = 0
            correct = 0
            total = 0

            if epoch > self.learning_rate_decay_start and self.learning_rate_decay_start >= 0:
                frac = (epoch - self.learning_rate_decay_start) // self.learning_rate_decay_every
                decay_factor = self.learning_rate_decay_rate ** frac
                current_lr = self.lr * decay_factor
                utils.set_lr(self.optimizer, current_lr)  # set the decayed rate
            else:
                current_lr = self.lr
            print('learning_rate: %s' % str(current_lr))

            for batch_idx, (inputs, targets) in enumerate(self.trainloader):
                if self.use_cuda:
                    inputs, targets = inputs.cuda(), targets.cuda()
                self.optimizer.zero_grad()
                inputs, targets = Variable(inputs), Variable(targets)
                for repeat_ in range(self.repeat_num):
                    # Generating adversarial examples
                    adversarial_attack = Adversarial_methods(inputs, targets, self.attack_iters, self.net, self.epsilon, self.alpha) 
                    delta = adversarial_attack.fgsm()
                    # Update network parameters
                    outputs = self.net(torch.clamp(inputs + delta, 0, 1))
                    loss = nn.CrossEntropyLoss()(outputs, targets)
                    loss.backward()
                    utils.clip_gradient(self.optimizer, 0.1)
                    self.optimizer.step()

                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += predicted.eq(targets.data).cpu().sum()

                utils.progress_bar(batch_idx, len(self.trainloader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
                    % (train_loss/(batch_idx+1), 100.*correct/total, correct, total))

            Train_acc = 100.*correct/total
        print("The final free_fast accuracy is :", Train_acc)
        torch.save(self.net.state_dict(), 'free_base_model.pt')
        return self.net
