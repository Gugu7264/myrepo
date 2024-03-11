# most usefull contrib ever

import re
import time
import datetime as dt
import jsontree
import pprint

if __name__ == "__main__":
    ###############################################
    def get_invite_code(text):
        regex = "(?:https?://)?discord(?:app\.com/invite|\.gg)/?[a-zA-Z0-9]+/?"
        result = re.findall(regex, text)
        print(result)
        result = result[0]
        if result[-1] == "/":
            result = result[:-1]
        code = ""
        found = 0
        for i in result[::-1]:
            if found: continue
            if i == "/":
                found = 1
            else:
                code += str(i)

        return code[::-1]
    ###############################################

    def reverse(msg):
        """Reverses a string"""
        debug = [msg]
        #    message = msg.replace('\\', '\\\\')
        message = msg.replace("@", "\@")

        debug.append(message)

        message = message.replace("`", "\`")

        debug.append(message)

        reversed = msg[::-1]

        reversed = reversed.replace("@", "\@").replace("`", "\`")

        print(f"Message: `{message}`\nReversed message: `{reversed}`\nDebug: ```\n{debug}```")
    ###############################################
    class not_in_list(BaseException):
        pass

    class not_in_stomach(BaseException):
        pass

    class actual_in_your_stomach(BaseException):
        pass

    class actual_in_this_stomach(BaseException):
        pass

    class already_eaten(BaseException):
        pass

    def dict_to_tuples(json):
        new_list = []
        for i in json:
            value = json[i]
            if type(value) == type({}):
                for k in value:
                    new_list.append((i, k))
                for j in dict_to_tuples(value):
                    new_list.append(j)
            else:
                new_list.append((i, value))
        return new_list

    def all_values_from_json(json):
        list = dict_to_tuples(json)
        values = []
        for i, j in list:
            values.append(i)
            values.append(j)
        return values

    def is_in_tuples(value, json):
        if value in all_values_from_json(json):
            return True
        else:
            return False

    def children(value, json):
        list = dict_to_tuples(json)
        if not is_in_tuples(value, json):
            raise not_in_list
        else:
            children = []
            for i, j in list:
                if i == value and j != "":
                    children.append(j)
            return children

    def parent(value, json):
        list = dict_to_tuples(json)
        if not is_in_tuples(value, json):
            raise not_in_list
        else:
            parent = None
            for i, j in list:
                if j == value:
                    parent = i
            return parent

    def _parents(value, json):
        if not is_in_tuples(value, json):
            raise not_in_list
        else:
            parents = []
            child = value
            part = ""
            while part is not None:
                part = parent(child, json)
                parents.append(part)
                child = part
            if None in parents:
                parents.remove(None)
            parents.reverse()
            return parents

    def path_to(value, json, last_step=1):
        if not is_in_tuples(value, json):
            raise not_in_list
        else:
            parents = _parents(value, json)
            path = json
            for i in parents:
                path = path[i]
            if last_step == 1:
                path = path[value]
            return path

    def vore(json, eater, eaten):
        if eater not in all_values_from_json(json):
            json[eater] = ""
        if eaten not in all_values_from_json(json):
            json[eaten] = ""
        if eaten in children(eater, json):
            raise actual_in_your_stomach
        if eaten in _parents(eater, json):
            raise actual_in_this_stomach
        if (eaten in json and eater in json) or eaten in children(parent(eater, json), json):
            pass
        elif eaten in all_values_from_json(json):
            raise already_eaten
        path = path_to(eater, json, 0)
        path_eaten = path_to(eaten, json, 0)
        if type(path[eater]) == type({}):
            path[eater].update({eaten: path_eaten.pop(eaten)})
        elif type(path[eater]) == type(""):
            path[eater] = {}
            path[eater].update({eaten: path_eaten.pop(eaten)})

    def spit(json, eater, eaten):
        if eaten not in children(eater, json):
            raise not_in_stomach
        path = path_to(eater, json, 0)
        path.update({eaten: path[eater].pop(eaten)})
        if len(path[eater]) == 0:
            path[eater] = ""

    text = input("URL: ")
    regex = "(?:https?://)?discord(?:app\.com/invite|\.gg)/?[a-zA-Z0-9]+/?"
    links = re.findall(regex, text)
    print(links[0])
    regex = "(?:https?://)?discord(?:app\.com/invite|\.gg)/?([a-zA-Z0-9]+)/?"
    searching = re.match(regex, links[0])
    print(searching.group(1))
