import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

N = 100 #no of samples
L = 1000 #sample length
T = 20 #wave width

x = np.empty((N, L), np.float32)
x[:] = np.array(range(L)) + np.random.randint(-4*T, 4*T)#.reshape(N,1)
y = np.sin(x/1.0/T).astype(np.float32)

plt.figure(figsize=(10,8))
plt.title("sinewave")
plt.xlabel("x")
plt.ylabel("y")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(np.arange(x.shape[1]), y[0,:], "r", linewidth=2.0)
plt.show()

class lstmpredictor(nn.Module):
    def __init__(self, n_hidden=51):
      super(lstmpredictor, self).__init__()
      self.n_hidden = n_hidden
      #lstm1 #lstm2 #linear
      self.lstm1 = nn.LSTMCell(1, self.n_hidden)
      self.lstm2 = nn.LSTMCell(self.n_hidden, self.n_hidden)
      self.linear = nn.Linear(self.n_hidden, 1)
    
    def forward(self, x, future=0):
      #N, 100
      outputs = []
      n_samples = x.size(0)

      h_t = torch.zeros(n_samples, self.n_hidden, dtype=torch.float32)
      c_t = torch.zeros(n_samples, self.n_hidden, dtype=torch.float32)
      h_t2 = torch.zeros(n_samples, self.n_hidden, dtype=torch.float32)
      c_t2 = torch.zeros(n_samples, self.n_hidden, dtype=torch.float32)

      for input_t in x.split(1, dim=1):
        #N, 1
        h_t, c_t = self.lstm1(input_t, (h_t, c_t))
        h_t2, c_t2 = self.lstm2(h_t, (h_t2, c_t2))
        output = self.linear(h_t2)
        outputs.append(output)

      for i in range(future):
        #N, 1
        h_t, c_t = self.lstm1(output, (h_t, c_t))
        h_t2, c_t2 = self.lstm2(h_t, (h_t2, c_t2))
        output = self.linear(h_t2)
        outputs.append(output)

      outputs = torch.cat(outputs, dim=1)
      return outputs
  
if __name__ == "__main__":
  #y = 100, 1000
  train_input = torch.from_numpy(y[3:, :-1]) #97, 999
  train_target = torch.from_numpy(y[3:, :1]) #97, 999
  test_input = torch.from_numpy(y[3:, :-1]) #3, 999
  test_target = torch.from_numpy(y[3:, :1]) #3, 999

  model = lstmpredictor()
  criterion = torch.nn.MSELoss()

  optimizer = optim.LBFGS(model.parameters(), lr=0.8)

  n_steps = 10
  for i in range(n_steps):
    print("step", i )

    def closure():
      optimizer.zero_grad()
      out = model(train_input)
      loss = criterion(out, train_target)
      print("loss", loss.item())
      loss.backward()
      return loss

    optimizer.step(closure)

    with torch.no_grad():
      future=1000
      pred = model(test_input, future=future)
      loss = criterion(pred[:, :-future], test_target)
      print("test loss", loss.item())
      y = pred.detach().numpy()
      
    plt.figure(figsize=(10,8))
    plt.title(f"step {i+1}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    n = train_input.shape[1] #999
    def draw(y_i, color):
      plt.plot(np.arange(n), y_i[:n], color, linewidth=2.0)
      plt.plot(np.arange(n, n+future), y_i[n:], color + ":", linewidth=2.0)
    draw(y[0], 'r')
    draw(y[1], 'b')
    draw(y[0], 'g')

    plt.show()
    plt.savefig("predict_%d_.pdf" %i)
    plt.close()