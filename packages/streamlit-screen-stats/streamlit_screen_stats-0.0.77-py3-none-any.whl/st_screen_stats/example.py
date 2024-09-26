import time
import streamlit as st
# from WindowScreenQuery.__init__ import WindowQuerySize, WindowQueryHelper
# from ScreenStWidgets.__init__ import StreamlitNativeWidgetScreen
from st_screen_stats import ScreenData, StreamlitNativeWidgetScreen, WindowQueryHelper 

# from st_screen_stats import ScreenData, StreamlitNativeWidgetScreen, WindowQuerySize # ScreenData, StreamlitNativeWidgetScreen

st.set_page_config(layout="wide")

with st.container(height=1, border=False):
    st.markdown(
        """
            <style>
                div[data-testid="element-container"]:has(iframe[title="st_screen_stats.WindowScreenQuery.st_window_query_size"]){
                        position:fixed;
                        top:-1000px;
                    }
            </style>

        """, unsafe_allow_html=True

    )


# with st.container(height=1, border=False):
helper_screen_stats = WindowQueryHelper(pause=None)
max_screen_  = helper_screen_stats.minimum_window_size(min_width=1249, default={"status":True})
min_screen_ = helper_screen_stats.maximum_window_size(max_width=1248, default={"status":False})
# helper_screen_stats.st_screen_data_window()
# max_width_window = helper_screen_stats.maximum_window_size(max_width=800, key="window_1")
st.write("large_screen",max_screen_, "small_screen",min_screen_)




# screenD = ScreenData(setTimeout=1000)
# screen_d = screenD.st_screen_data_window()

# st.write(screen_d)

# # test_func_ = WindowQuerySize()
# # result_ = test_func_.mediaQuery(mediaMatchQ="(min-width: 1439px)", key="testing_here") 


# # st.write("Hii")
# # st.status("How are you")

# # if result_["status"]: # or st.session_state["testing_here"]["status"]: 
# #     st.success("Yayy")
#     # st.write(result_["status"])

# # time.sleep(6)

# while st.session_state["testing_here"]["status"] == None:
   
#     if type(st.session_state["testing_here"]["status"]) == True:
#         break
#     time.sleep(0.25)

# if st.session_state["testing_here"]["status"]:
#     st.success("Yayy")
#     st.write(st.session_state["testing_here"]["status"])


# # @st.experimental_fragment
# # def get_screen_size():

# #     test_func_ = WindowQuerySize()
# #     result_ = test_func_.mediaQuery(mediaMatchQ="(min-width: 1439px)", default={"status":None}, key="testing_here") 

# #     if result_["status"] != None:
# #         st.rerun()


# # if "testing_here" not in st.session_state:
# #     get_screen_size()

# # result_ = st.session_state["testing_here"]
# # while result_ == None:
# #     if type(result_["status"]) == True:
# #         break
# #     time.sleep(0.25)
    

# # st.write(st.session_state["testing_here"])






# st.link_button("Go away!", url="http://localhost:8502/")

# # import gtk, pygtk

# # window = gtk.Window()
# # screen = window.get_screen()