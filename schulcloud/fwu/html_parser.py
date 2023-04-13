from bs4 import BeautifulSoup
import converter.env as env


def get_data(class_name: str, s: BeautifulSoup):
    if not class_name == "pname" and not class_name == "ptext" and not class_name == "player_outer":
        raise RuntimeError(
            f'False value "{class_name}" for class_name in get_data(). Options: pname, ptext, player_outer')

    html_snippet = s.find_all("div", class_=class_name)
    html_snippet = str(html_snippet)

    if class_name == "player_outer":
        index_start = html_snippet.index("(", 0) + 1
        index_end = html_snippet.index(")", 2)
    else:
        index_start = html_snippet.index(">", 0) + 1
        index_end = html_snippet.index("<", 2)

    result = html_snippet[index_start:index_end]
    result = result.strip()

    if class_name != "player_outer":
        validate_result(class_name, result)

    return result


def validate_result(class_name: str, result: str):
    data_definition = ""

    if class_name == "pname":
        data_definition = "Title"
    elif class_name == "ptext":
        data_definition = "Description"

    if result is None or result == "" or result == " ":
        raise RuntimeError(f'{data_definition} not found in class "{class_name}"')


def main():
    # add your local path to your index.html in your .env (LOCAL_PATH="local/path/index.html")
    local_path = env.get('LOCAL_PATH')
    html_file = open(local_path, "r")

    s = BeautifulSoup(html_file.read(), 'lxml')

    title = get_data("pname", s)
    description = get_data("ptext", s)
    thumbnail = get_data("player_outer", s)

    # Output
    print(f'Title: {title}')
    print(f'Description: {description}')
    print(f'Thumbnail: {thumbnail}')


if __name__ == '__main__':
    main()
