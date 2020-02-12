
from django.db import models
from datetime import datetime



# class UserProfile(models.Model):
#     user_id=models.AutoField(primary_key=True)
#     Username = models.CharField( max_length=100)
#     Password = models.CharField( max_length=100)
#     Email = models.EmailField(max_length=70)
       
#     class Meta:
#         db_table ='UserProfile'
    
#     def __str__(self):
#         return "{}".format(self.user_id)

class UserProfileInfo(models.Model):
    user_id=models.AutoField(primary_key=True)
    Username = models.CharField( max_length=100)
    Password = models.CharField( max_length=100)
    Email = models.EmailField(max_length=70)
       
    class Meta:
        db_table ='UserProfileInfo'
    
    def __str__(self):
        return "{}".format(self.user_id)


class Csv_file(models.Model):
    user=models.ForeignKey(UserProfileInfo,null=True, on_delete = models.CASCADE)
    file_id=models.AutoField(primary_key=True)
    Target = models.CharField(max_length = 10000)
    Pickel_file = models.FileField()
    # UserProfileInfo=models.ForeignKey(UserProfileInfo, on_delete = models.CASCADE, null=True, verbose_name=UserProfileInfo)
    # UserProfileInfo = models.ForeignKey(UserProfileInfo, on_delete = models.PROTECT, null=True, verbose_name=UserProfileInfo)
  
    # Updated_date = models.DateTimeField(default = datetime.now())



    class Meta:
        db_table = 'Csv_file'

    def __str__(self):
       return "{}".format(self.file_id)
       

class Csv_Features(models.Model):
    
    file = models.ForeignKey(Csv_file,null=True, on_delete =  models.CASCADE)
    Features = models.CharField(max_length = 10000)
        
    class Meta:
        db_table = 'Csv_Features'

    def __str__(self):
       return "{}".format(self.Features)


    







