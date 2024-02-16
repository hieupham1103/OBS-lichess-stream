import obspython as obs

BOARD_ID = "hYi4B3Fh"
CUSTOM_CSS_BOARD = """#top{
  display: none;
}
* {
  visibility: hidden;
}
.manipulable *{
  visibility: visible;
}

body{
  background: rgba(76, 175, 80, 0);
  overflow: hidden;
}

.main-board{
  height: 100vh;
  width: 100vh;
}

"""

CUSTOM_CSS_TIMER = """#top{
  display: none;
}
* {
  visibility: hidden;
}
.rclock-bottom *{
  visibility: visible;
}

body{
  background: rgba(76, 175, 80, 0);
  overflow: hidden;
}

"""

white_source = ""
black_source = ""
white_timer = ""
black_timer = ""


description = """This is the script used to setup the chessboard stream on Lichess.
By Phạm Đinh Trung Hiếu (@hieupham1103)
"""

def script_description():    
    return description


def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "CUSTOM_CSS_BOARD", CUSTOM_CSS_BOARD)
    obs.obs_data_set_default_string(settings, "CUSTOM_CSS_TIMER", CUSTOM_CSS_TIMER)
    
    
def script_properties():
    props = obs.obs_properties_create()
    
    
    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)

    #====================================================
    obs.obs_properties_add_text(props, "BOARD_ID", "Game ID", obs.OBS_TEXT_DEFAULT)
    #====================================================
    white_board_source = obs.obs_properties_add_list(
        props,
        "white_source",
        "White Chess Board",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_type = obs.obs_source_get_id(source)
            if source_type == "browser_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(white_board_source, name, name)
    
    
    black_board_source = obs.obs_properties_add_list(
        props,
        "black_source",
        "Black Chess Board",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_type = obs.obs_source_get_id(source)
            if source_type == "browser_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(black_board_source, name, name)
                
    #====================================================
    
    black_board_source = obs.obs_properties_add_list(
        props,
        "white_timer",
        "White Timer",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_type = obs.obs_source_get_id(source)
            if source_type == "browser_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(black_board_source, name, name)
                
    black_board_source = obs.obs_properties_add_list(
        props,
        "black_timer",
        "Black Timer",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_type = obs.obs_source_get_id(source)
            if source_type == "browser_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(black_board_source, name, name)
    
    
    #====================================================
    
    obs.obs_properties_add_text(props, "CUSTOM_CSS_BOARD", "CSS CHESS BOARD", obs.OBS_TEXT_MULTILINE)
    obs.obs_properties_add_text(props, "CUSTOM_CSS_TIMER", "CSS CHESS TIMER", obs.OBS_TEXT_MULTILINE)
    
    #====================================================
    
    
    return props


def script_update(settings):
    global BOARD_ID
    global white_source
    global black_source
    global white_timer
    global black_timer
    global CUSTOM_CSS_BOARD
    BOARD_ID = obs.obs_data_get_string(settings, "BOARD_ID")
    CUSTOM_CSS_BOARD = obs.obs_data_get_string(settings, "CUSTOM_CSS_BOARD")
    white_source = obs.obs_data_get_string(settings, "white_source")
    black_source = obs.obs_data_get_string(settings, "black_source")
    white_timer = obs.obs_data_get_string(settings, "white_timer")
    black_timer = obs.obs_data_get_string(settings, "black_timer")
    

def refresh_pressed(props, prop):
    update_board(white_source, "https://lichess.org/" + BOARD_ID, CUSTOM_CSS_BOARD)
    update_board(black_source, "https://lichess.org/" + BOARD_ID + "/black/", CUSTOM_CSS_BOARD)
    update_board(white_timer, "https://lichess.org/" + BOARD_ID, CUSTOM_CSS_TIMER)
    update_board(black_timer, "https://lichess.org/" + BOARD_ID + "/black/", CUSTOM_CSS_TIMER)


def update_board(board, url, css):
    source = obs.obs_get_source_by_name(board)
    
    if source is not None:
        # data = obs.obs_data_get_json(obs.obs_source_get_settings(source))
        # print(data)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "url", url)
        obs.obs_data_set_string(settings, "css", css)
        color_key = obs.obs_source_get_filter_by_name(source, "ChromaKey")
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)