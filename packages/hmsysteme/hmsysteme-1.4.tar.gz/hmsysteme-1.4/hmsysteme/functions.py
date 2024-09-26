import multiprocessing
import pygame




import pickle
import os


path = os.path.realpath(__file__)
path = path.replace('functions.py', '')


def put_rgbcolor(color):
    file = open((os.path.join(path, "hmrgb")), 'wb')
    pickle.dump(color, file)
    file.close()


def get_rgbcolor():
    try:
        file = open((os.path.join(path, "hmrgb")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmrgb", False)
            return q
        else:
            return False
    except:
        return False


def get_path():
    return path


def screenshot_refresh():
    try:
        file = open((os.path.join(path, "hmscreen")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmscreen", False)
            return True
        else:
            return False
    except:
        return False


def take_screenshot_parallel(screen):
    def create_screenshot(screen):
        try:
            os.remove(os.path.join(path, "screencapture.jpg"))
        except:
            pass
        pygame.image.save(screen, os.path.join(path, "screencapture.jpg"))
        file = open((os.path.join(path, "hmscreen")), 'wb')
        pickle.dump(True, file)
        file.close()

    t = multiprocessing.Process(target=create_screenshot, args=(screen,))
    t.start()
    # t.join()


def take_screenshot(screen):
    try:
        os.remove(os.path.join(path, "screencapture.jpg"))
    except:
        True
    pygame.image.save(screen, os.path.join(path, "screencapture.jpg"))
    file = open((os.path.join(path, "hmscreen")), 'wb')
    pickle.dump(True, file)
    file.close()


# def game_isactive():
#     try:
#         file = open((os.path.join(path, "hmsys")), 'rb')
#         q = pickle.load(file)
#         file.close()
#         if q != True:
#             clear_pickle("hmsys", True)
#             return False
#         else:
#             return True
#     except:
#         return True
#
#
# def close_pygame():
#     file = open((os.path.join(path, "hmsys")), 'wb')
#     pickle.dump(False, file)
#     file.close()


def game_isactive():
    if os.environ["hm_GameIsActive"] == "1":
        return True
    else:
        return False


def close_game():
    os.environ["hm_GameIsActive"] = "0"

def open_game():
    os.environ["hm_GameIsActive"] = "1"

def check_ifdebug():
    import io
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return False
    except Exception: pass
    return True



def clear_pickle(filename, val):
    file = open((os.path.join(path, filename)), 'wb')
    pickle.dump(val, file)
    file.close()





def put_pos(pos):
    file = open((os.path.join(path, "hmpos")), 'wb')
    pickle.dump(pos, file)
    file.close()


def get_size():
    return (1360, 768)


def get_pos():
    try:
        file = open((os.path.join(path, "hmpos")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmpos", False)
            return q
        else:
            return False
    except:
        return False


def put_temp(temp):
    file = open((os.path.join(path, "hmtemp")), 'wb')
    pickle.dump(temp, file)
    file.close()


def get_temp():
    try:
        file = open((os.path.join(path, "hmtemp")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmtemp", False)
            return q
        else:
            return False
    except:
        return False


def put_button_names(names):
    file = open((os.path.join(path, "hmbuttons")), 'wb')
    pickle.dump(names, file)
    file.close()


def get_button_names():
    try:
        file = open((os.path.join(path, "hmbuttons")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmbuttons", False)
            return q
        else:
            return False
    except:
        return False


def put_hit():
    file = open((os.path.join(path, "hmhit")), 'wb')
    pickle.dump(True, file)
    file.close()


def hit_detected():
    try:
        file = open((os.path.join(path, "hmhit")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmhit", False)
            return q
        else:
            return False
    except:
        return False


def get_action():
    try:
        file = open((os.path.join(path, "hmaction")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmaction", False)
            return q
        else:
            return False
    except:
        return False


def put_action(number):
    file = open((os.path.join(path, "hmaction")), 'wb')
    pickle.dump(number, file)
    file.close()


def put_playernames(playernames):
    file = open((os.path.join(path, "hmplayers")), 'wb')
    pickle.dump(playernames, file)
    file.close()


def get_playernames():
    try:
        file = open((os.path.join(path, "hmplayers")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            w = []
            for i in range(0, len(q)):
                if q[i][1] == True:
                    w.append(q[i][0])
            return w
        else:
            return False
    except:
        return False


def clear_all():
    os.environ["hm_GameIsActive"] = "0"
    clear_pickle("hmhit", False)
    clear_pickle("hmpos", False)
    clear_pickle("hmplayers", False)
    clear_pickle("hmscreen", False)
    clear_pickle("hmrgb", False)
    clear_pickle("hmtemp", False)
    clear_pickle("hmaction", False)
    clear_pickle("hmbuttons", False)

