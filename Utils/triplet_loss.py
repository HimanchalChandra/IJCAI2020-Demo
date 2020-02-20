import torch
from torch.autograd import Function
from torch.nn.modules.distance import PairwiseDistance


class TripletLoss(Function):

    def __init__(self, margin):
        super(TripletLoss, self).__init__()
        self.margin = margin
        self.calc_dist = PairwiseDistance(2)

    def forward(self, anchor, positive, negative):
        pos_dist = self.calc_dist.forward(anchor, positive)
        neg_dist = self.calc_dist.forward(anchor, negative)

        hinge_dist = torch.clamp(self.margin + pos_dist - neg_dist, min=0.0)
        loss = torch.mean(hinge_dist)

        return loss
