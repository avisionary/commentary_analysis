import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



class plot_formations():
    """
        Class to dynamically plot formations of home and away team
    """

    def __init__(self,home_formations,away_formations) -> None:

        self.home_formations = home_formations
        self.away_formations = away_formations

    
    
    def __str__(self) -> str:
        return f"Home Formation: {self.home_formations}; Away Formation: {self.away_formations}"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({str(self)})>"
    

    def set_coordiantes(self):
        x_axis_start1 = 0
        x_axis_end1 = 100

        x_axis_start2 = 100
        x_axis_end2 = 200

        y_axis_start = 0
        y_axis_end = 100


        y = []
        list_form1 = self.home_formations.split("-")
        list_form2 = self.away_formations.split("-")

        list_form1.insert(0,"1")
        list_form2.insert(0,"1")

        list_form2 = list_form2[::-1]
        print(list_form2)

        final_list = list_form1 + list_form2
        print(final_list)


        x_axis_split = len(list_form1) + 1
        start_pos_x = (x_axis_end1 - x_axis_start1)/x_axis_split
        #print(start_pos_x)
        x_axis = x_axis_start1
        y_axis = y_axis_start
        for position in list_form1:
            position = int(position)
            x_axis = x_axis + start_pos_x
            print(f"Num {position}")
            print(f"X_axis : {x_axis}")
            y_axis_split = position + 1
            start_pos_y = (y_axis_end - y_axis_start)/y_axis_split
            
            for player in range(position):
                
                y_axis = y_axis + start_pos_y
                print(f"Y_Axis : {y_axis}")
                y.append((x_axis,y_axis))
            y_axis = y_axis_start

        x_axis_split = len(list_form2) + 1
        start_pos_x = (x_axis_end2 - x_axis_start2)/x_axis_split
        #print(start_pos_x)
        x_axis = x_axis_start2
        y_axis = y_axis_start
        for position in list_form2:
            position = int(position)
            x_axis = x_axis + start_pos_x
            print(f"Num {position}")
            print(f"X_axis : {x_axis}")
            y_axis_split = position + 1
            start_pos_y = (y_axis_end - y_axis_start)/y_axis_split
            
            for player in range(position):
                
                y_axis = y_axis + start_pos_y
                print(f"Y_Axis : {y_axis}")
                y.append((x_axis,y_axis))
            y_axis = y_axis_start
        
        self.formation = np.array(y)

        return self.formation
    

    def fomation_plot(self,formation):
        fig, ax = plt.subplots(figsize=(10, 5))
        img = plt.imread("../../figures/images/pitch.jpeg")

        plt.xlim(0, 200)
        plt.ylim(0, 100)

        mask = formation[:, 0] > 100  # Boolean mask for x-axis points greater than 100

        ax.scatter(formation[~mask, 0], formation[~mask, 1], s=450, edgecolors='black', linewidths=2,c = "blue") # plot points with x-axis value <= 100

        ax.scatter(formation[mask, 0], formation[mask, 1], s=450, edgecolors='black', linewidths=2, c='red') # plot points with x-axis value > 100 in red color

        ax.imshow(img, extent=[0, 200, 0, 100])
        plt.axis("off")
        plt.show()


    def streamlit_plot(self,formation):
        fig, ax = plt.subplots(figsize=(10, 5))
        img = plt.imread("../../figures/images/pitch.jpeg")

        plt.xlim(0, 200)
        plt.ylim(0, 100)

        mask = formation[:, 0] > 100  # Boolean mask for x-axis points greater than 100

        ax.scatter(formation[~mask, 0], formation[~mask, 1], s=450, edgecolors='black', linewidths=2,c = "blue") # plot points with x-axis value <= 100

        ax.scatter(formation[mask, 0], formation[mask, 1], s=450, edgecolors='black', linewidths=2, c='red') # plot points with x-axis value > 100 in red color

        ax.imshow(img, extent=[0, 200, 0, 100])
        plt.axis("off")
        st.pyplot(fig)


                