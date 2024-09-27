from opencv_helper.cv import OpencvHelper

print(OpencvHelper.find_pic("1.png", "2.png"))
print(OpencvHelper.find_pic("1.png", "3.png", sim=0.7))
print(OpencvHelper.find_pic("1.png", "4.png", sim=0.6))
