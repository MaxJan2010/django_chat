from django.db import models
from django.contrib.auth.models import User
from .room import Room


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    other = models.ForeignKey(User, on_delete=models.CASCADE, related_name="other_contacts")
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.user.id < self.other.id:
            return f"contact-{self.user.id}-{self.other.id}"
        else:
            return f"contact-{self.other.id}-{self.user.id}"


class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests")
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user.id < self.other.id:
            return f"friend-request-{self.user.id}-{self.other.id}"
        else:
            return f"friend-request-{self.other.id}-{self.user.id}"

    def save(self, *args, **kwargs):
        if self.accepted == True:
            if self.user.id < self.other.id:
                name=f"room-{self.user.id}-{self.other.id}"
                room, _ = Room.objects.get_or_create(name=name)
            else:
                name=f"room-{self.other.id}-{self.user.id}"
                room, _ = Room.objects.get_or_create(name=name)

            Contact.objects.get_or_create(user=self.user, other=self.other, room=room)
            Contact.objects.get_or_create(user=self.other, other=self.user, room=room)

        return super(FriendRequest, self).save(*args, **kwargs)