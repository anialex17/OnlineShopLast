from django.db import models


class TermsOrder(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='about_order')


class SendMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Անուն")
    lastname = models.CharField(max_length=100, verbose_name="Ազգանուն")
    email = models.EmailField(verbose_name="Էլեկտրոնային հասցե")
    message = models.TextField(verbose_name="Նամակ")
    file = models.FileField(upload_to='files', blank=True, verbose_name="Ֆայլ")
    created_at = models.DateTimeField(auto_now_add=True,null=True, verbose_name="Ստեղծվոլ է")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Նամակ'
        verbose_name_plural = 'Նամակներ'
        ordering = ['created_at']


class Contact(models.Model):
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone_number_1 = models.CharField(max_length=50)
    phone_number_2 = models.CharField(max_length=50, blank=True)
    phone_number_3 = models.CharField(max_length=50, blank=True)

