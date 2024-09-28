from drjit.cuda.ad import Int as IntD, Float as FloatD, Matrix4f as Matrix4fD, Array3f as Vector3fD, Array2f as Vector2fD
import torch 

a = torch.arange(16).reshape(4, 4).float().cuda()

b = Matrix4fD(a.reshape(1, 4, 4))
print(b)
