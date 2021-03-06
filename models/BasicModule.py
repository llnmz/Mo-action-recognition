# coding:utf8

import torch as t
import time


class BasicModule(t.nn.Module):
    '''
    封装了nn.Module,主要是提供了save和load两个方法
    '''

    def __init__(self):
        super(BasicModule, self).__init__()
        self.model_name = str(type(self))  # 默认名字

    def load(self, path, change_opt=True):
        data = t.load(path)
        if 'opt' in data:
            # old_opt_stats = self.opt.state_dict()
            if change_opt:
                self.opt.parse(data['opt'], print_=False)
                self.opt.embedding_path = None
                self.__init__(self.opt)
            # self.opt.parse(old_opt_stats,print_=False)
            self.load_state_dict(data['d'])
        else:
            self.load_state_dict(data)
        return self.cuda()

    def save(self, name=None, new=False):
        prefix = 'checkpoints/' + self.model_name + '_' + self.opt.type_ + '_'
        if name is None:
            name = time.strftime('%m%d_%H:%M:%S.pth')
        path = prefix + name

        if new:
            data = {'opt': self.opt.state_dict(), 'd': self.state_dict()}
        else:
            data = self.state_dict()

        t.save(data, path)
        return path

    def get_optimizer(self, lr1, lr2=0, weight_decay=0):
        encoder_params = list(map(id, self.encoder.parameters()))
        lstm_params = filter(lambda p: id(p) not in encoder_params,
                             self.parameters())

        optimizer = t.optim.Adam([
            dict(params=lstm_params, weight_decay=weight_decay, lr=lr1),
            {'params': self.encoder.parameters(), 'lr': lr2}
        ])
        return optimizer

    # def save2(self,name=None):
    #     prefix = 'checkpoints/' + self.model_name + '_'
    #     if name is None:
    #         name = time.strftime('%m%d_%H:%M:%S.pth')
    #     path = prefix+name
    #     data = {'opt':self.opt.state_dict(),'d':self.state_dict()}
    #     t.save(data, path)
    #     return path
    # # def load2(self,path):
    # #     data = t.load(path)
    # #     self.__init__(data['opt'])
    # #     self.load_state_dict(data['d'])
