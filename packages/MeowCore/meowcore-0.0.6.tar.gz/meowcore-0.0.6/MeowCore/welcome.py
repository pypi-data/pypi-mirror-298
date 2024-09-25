# A helper function for Telegram Category uses

import aiohttp
from aiofiles import open as aio_open
import asyncio
from PIL import Image, ImageDraw, ImageOps, ImageFont
import os
import requests


class WelcomeFunc:
    async def check_welcome_template(self, template_id):
        if template_id in self.WELCOME_TEMPLATE:
            data = self.WELCOME_TEMPLATE[template_id]
            return data
        else:
            return None

    def load_welcome(self, all_welcome_id):
        if self.category != "telegram":
            return
        loop = asyncio.get_event_loop()
        loop.create_task(self.background_load_welcome(all_welcome_id))
        # await self.background_load_welcome(all_welcome_id)

    async def background_load_welcome(self, all_welcome_id):
        """
        Asynchronously fetch welcome templates and download background images.
        
        :Raises ConnectionError: If the request to fetch templates fails.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.apiurl}/fetch_welcome_templates",
            headers=headers,
            json={"data": all_welcome_id}
        )
        if response.status_code != 200:
            raise ConnectionError(f"Error connecting to {self.apiurl}")
        self.WELCOME_TEMPLATE = response.json()["data"]
        print(response.json()["error"])
        failedd = response.json()["failed"]
        passsed = response.json()["passed"]
        print(f"Welcome Template load: Failed- {failedd} | Passed- {passsed}")

        async with aiohttp.ClientSession() as session:
            for template_id, template_data in self.WELCOME_TEMPLATE.items():
                template_bg_url = template_data["data"]["bg_url"]         
                try:
                    async with session.get(template_bg_url) as resp:
                        if resp.status == 200:
                            os.makedirs(f"resources/template", exist_ok=True)
                            file_path = os.path.join(f"resources/template/{template_id}bgimage.png")
                            async with aio_open(file_path, 'wb') as f:
                                async for chunk in resp.content.iter_chunked(8192):
                                    await f.write(chunk)
                        else:
                            print(f"Failed to download {template_bg_url}, status code: {resp.status}")
                except Exception as e:
                    print(f"Error downloading {template_bg_url}: {e}")

    async def build_welcome(self, template_id, user, chat, data):
        """
        Builds a welcome image by overlaying user and chat profile pictures, and
        adding personalized text over a background image.
        """
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        user_name = user.username
        chat_id = chat.id
        chat_title = chat.title
        build_data = data["data"]

        bg_path = f"resources/template/{template_id}bgimage.png"
        user_pfp = build_data["user_pfp"]
        chat_pfp = build_data["chat_pfp"]
        
        tempbg_open = Image.open(bg_path)

        # User Profile Picture
        if user_pfp:
            user_pfp_data = build_data["user_pfp_data"]
            user_pfp = f"downloads/{user_id}userpfp.jpg"
            user_pfp_img, user_pfp_pos = await self.circular_crop(
                user_pfp, 
                user_pfp_data["size"], 
                user_pfp_data["circle"], 
                user_pfp_data["location"]
            )
            tempbg_open.paste(user_pfp_img, user_pfp_pos, user_pfp_img)

        # Chat Profile Picture
        if chat_pfp:
            chat_pfp_data = build_data["chat_pfp_data"]
            chat_pfp = f"downloads/{user_id}chatpfp.jpg"
            chat_pfp_img, chat_pfp_pos = await self.circular_crop(
                chat_pfp, 
                chat_pfp_data["size"], 
                chat_pfp_data["circle"], 
                chat_pfp_data["location"]
            )
            tempbg_open.paste(chat_pfp_img, chat_pfp_pos, chat_pfp_img)

        # Add Text
        draw = ImageDraw.Draw(tempbg_open)
        all_text_data = build_data["text_data"]
    
        for text_data in all_text_data:
            font_name = text_data["font"]["font"]
            font_path = f"resources/template/fonts/{font_name}"
            try:
                font = ImageFont.truetype(font_path, size=text_data["font"]["size"])
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Font file not found: {font_path}. Please ensure the font file exists.")
            except OSError as e:
                raise OSError(f"Error loading font from: {font_path}. The font may be corrupted or invalid.")
            except Exception as e:
                raise Exception(f"An unexpected error occurred while importing fonts: {str(e)}")
           
            text = text_data["text"]
            if text == "$user_id":
                text = str(user_id)
            elif text == "$first_name":
                text = first_name
        
            await self.add_text(
                draw, 
                text, 
                (text_data["horizontal"], text_data["vertical"]), 
                font, 
                text_data["font"]["color"]
            )

        # Save the final image
        tempbg_open.save(f"resources/{chat_id}complete.png")

        # clean up memory
        try:
            tempbg_open.close()
            if user_pfp:
                user_pfp_img.close()
            if chat_pfp:
                chat_pfp_img.close()
        except:
            pass
        return
            
    async def circular_crop(self, image_path, size, circle_scale, location):
        """
        Helper function to crop an image into a circular shape and resize it.
        """
        img = Image.open(image_path).resize((640, 640))
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        circular_img = ImageOps.fit(img, mask.size)
        circular_img.putalpha(mask)
        width, height = circular_img.size
        new_width = int(width * circle_scale)
        new_height = int(height * circle_scale)
        circular_img = circular_img.resize((new_width, new_height))
        return circular_img, (location["horizontal"], location["vertical"])

    async def add_text(self, draw, text, position, font, color):
        """
        Helper function to draw text on an image.
        """
        draw.text(position, text, fill=color, font=font)

