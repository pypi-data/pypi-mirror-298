from yyyutils.auto_utils.auto_click.auto_click_by_image_utils import AutoClickGenerator
from yyyutils.window_utils import WindowUtils
if __name__ == '__main__':
    generator = AutoClickGenerator("QQ")
    generator.add_icons(['1.png', '2.png']).click()
