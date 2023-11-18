import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources


class Cloudinary:
    cloudinary.config(
        cloud_name="dm4renyes",
        api_key="352973869923155",
        api_secret="10vpZUBl6Oh314SohJVLvPcyAxU"
    )

    def upload_image(self, image, name, code):
        id = f"{name}_{code}"
        upload_result = cloudinary.uploader.upload(image,
                                                   public_id=id)
        return upload_result["url"]

    def delete_image(self, public_url):
      
        public_id = cloudinary_url(public_url)[0]
        delete_result = delete_resources([public_id])
        if delete_result.get('deleted', 0) > 0:
            return True
        else:
            return False