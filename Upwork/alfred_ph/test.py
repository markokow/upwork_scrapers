from TikTokApi import TikTokApi
from attr import has

api = TikTokApi(custom_verify_fp="verify_l92orvbi_yorJ2uWe_vqK4_4GxQ_BbO8_kmsPBJfrcFPb")

video = api.by_hashtag(hashtag="rex", count = 30)

print(video)

# c)


# for comment in video.comments():
    # print(comment.text)