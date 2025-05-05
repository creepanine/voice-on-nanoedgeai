from __future__ import print_function
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torchvision
import transforms as transforms
import numpy as np
import os
import argparse
import utils
from CKplus import CKplus
from torch.autograd import Variable
from Networks import *
from adversarial_training import Adversarial_Trainings
from config import get_args
from test_accuracy import*
from time import clock
from FER2013 import FER2013


opt = get_args()
best_Test_acc = 0  # best PrivateTest accuracy
best_Test_acc_epoch = 0
start_epoch = 0  # start from epoch 0 or last checkpoint epoch

learning_rate_decay_start = 70  # 50
learning_rate_decay_every = 5   # 5
learning_rate_decay_rate = 0.9   # 0.9

cut_size = 44

path = os.path.join(opt.dataset + '_' + opt.model, 'mn')
file_name = 'repeat_num={}'.format(opt.repeat_num)

# Data
print('==> Preparing data..')
transform_train = transforms.Compose([
    transforms.RandomCrop(cut_size),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])

transform_test = transforms.Compose([
    transforms.TenCrop(cut_size),
    transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
])

trainset = FER2013(split = 'Training', transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=opt.bs, shuffle=True, num_workers=0)
testset = FER2013(split = 'PublicTest', transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=opt.bs, shuffle=False, num_workers=0)


# Model
if opt.model == 'VGG19':
    net = VGG('VGG19')
    # multi_net = VGG_multi('VGG19')
else:
    net = ResNet18()
    # multi_net = ResNet18_multi()

if opt.resume:
    # Load checkpoint.
    print('==> Resuming from checkpoint..')
    path = 'model/VGG19/model.pt'
    checkpoint = torch.load(os.path.join(path))
    net.load_state_dict(checkpoint)
else:
    print('==> Building model..')

path_multi = 'model/VGG19/multi_model.t7'
# multi_net.load_state_dict(torch.load(path_multi))

use_cuda = torch.cuda.is_available()
if use_cuda:
    net.cuda()
    # multi_net.cuda()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=opt.lr, momentum=0.9, weight_decay=5e-4)


if __name__ == '__main__':
    start_time = clock()
    adversarial_training = Adversarial_Trainings(opt.repeat_num,trainloader, use_cuda, opt.attack_iters, net, multi_net, opt.epsilon, opt.alpha, learning_rate_decay_start, learning_rate_decay_every, learning_rate_decay_rate, opt.lr, opt.multi_lr, opt.save_path, opt.gamma1, opt.gamma2)
    trainned_net = adversarial_training.Stardard_Training(opt.epoch)
    end_time = clock()

    cost_time = end_time - start_time
    attack_dict = {'attack_iters': 1 , 'net': trainned_net, 'epsilon': 0.008, 'alpha':0.007}
    Test_acc = test(use_cuda, testloader, trainned_net, criterion, None)
    Test_acc_adv = test_adv(use_cuda, testloader, trainned_net, criterion, attack_dict)
    Test_acc_avg_adv = test_adv(use_cuda, testloader, trainned_net, criterion, attack_dict)
    if not os.path.exists(opt.save_path):
        os.makedirs(opt.save_path)
    # torch.save(trainned_net.state_dict(), os.path.join(opt.save_path,'model.pt'))
    print('Run time: ', cost_time)
    print("Test_acc: %0.3f" % Test_acc)
    print('Test_acc_adv: %0.3f' % Test_acc_adv)
    print('Test_acc_avg_adv: %0.3f' % Test_acc_avg_adv)
