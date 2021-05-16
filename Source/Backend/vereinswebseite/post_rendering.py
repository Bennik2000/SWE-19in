import re

import markdown


class MarkdownRenderer:

    def render(self, content: str) -> str:
        return markdown.markdown(content, extensions=["extra"])

    def get_all_images(self, content: str):
        # This regex matches all images in a markdown document
        all_image_urls = re.findall(r'!\[.*?]\(([^ ]+).*?\)', content)
        all_image_names = []

        for url in all_image_urls:

            # This regex extracts the image name from an image url
            name = re.findall(r'.*/([a-zA-Z0-9]+\.[a-zA-Z0-9]+)', url)

            if len(name) == 1:
                all_image_names.append(name[0])

        return all_image_names


post_renderer = MarkdownRenderer()
