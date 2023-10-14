import cloudinary
import cloudinary.uploader


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
