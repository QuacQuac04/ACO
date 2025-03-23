import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VRPSTW_Simple:
    def __init__(self):
        # Tạo cửa sổ chính
        self.window = tk.Tk()
        self.window.title("Giải bài toán VRPSTW")
        
        # Tạo khung nhập liệu
        self.create_input_frame()
        
        # Tạo khung hiển thị kết quả
        self.create_result_frame()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.window, text="Thông số đầu vào")
        input_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Tạo các ô nhập liệu
        ttk.Label(input_frame, text="Số khách hàng:").grid(row=0, column=0)
        self.customers_entry = ttk.Entry(input_frame)
        self.customers_entry.grid(row=0, column=1)
        
        ttk.Label(input_frame, text="Số xe:").grid(row=1, column=0)
        self.vehicles_entry = ttk.Entry(input_frame)
        self.vehicles_entry.grid(row=1, column=1)
        
        # Nút giải bài toán
        ttk.Button(input_frame, text="Giải bài toán", command=self.solve_problem).grid(row=2, column=0, columnspan=2, pady=10)
        
    def create_result_frame(self):
        result_frame = ttk.LabelFrame(self.window, text="Kết quả")
        result_frame.grid(row=0, column=1, padx=10, pady=10)
        
        # Tạo vùng vẽ đồ thị
        self.fig = plt.Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack()
        
    def solve_problem(self):
        try:
            # Lấy dữ liệu từ người dùng
            n_customers = int(self.customers_entry.get())
            n_vehicles = int(self.vehicles_entry.get())
            
            # Tạo dữ liệu mẫu
            self.create_sample_data(n_customers)
            
            # Tạo tuyến đường mẫu (đơn giản hóa)
            routes = self.create_simple_routes(n_customers, n_vehicles)
            
            # Hiển thị kết quả
            self.show_results(routes)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
            
    def create_sample_data(self, n_customers):
        # Tạo tọa độ ngẫu nhiên cho khách hàng và kho
        self.locations = np.random.rand(n_customers + 1, 2) * 100
        
    def create_simple_routes(self, n_customers, n_vehicles):
        # Chia khách hàng đều cho các xe (đơn giản hóa)
        routes = []
        customers_per_vehicle = n_customers // n_vehicles
        
        for i in range(n_vehicles):
            start = i * customers_per_vehicle + 1
            end = start + customers_per_vehicle
            if i == n_vehicles - 1:
                end = n_customers + 1
            route = [0] + list(range(start, end)) + [0]
            routes.append(route)
            
        return routes
    
    def show_results(self, routes):
        # Xóa đồ thị cũ
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Vẽ khách hàng và kho
        ax.scatter(self.locations[1:,0], self.locations[1:,1], c='blue', label='Khách hàng')
        ax.scatter([self.locations[0,0]], [self.locations[0,1]], c='red', marker='s', label='Kho')
        
        # Vẽ tuyến đường
        colors = ['g', 'r', 'c', 'm', 'y']
        for i, route in enumerate(routes):
            color = colors[i % len(colors)]
            for j in range(len(route)-1):
                start = self.locations[route[j]]
                end = self.locations[route[j+1]]
                ax.plot([start[0], end[0]], [start[1], end[1]], c=color)
        
        ax.legend()
        self.canvas.draw()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = VRPSTW_Simple()
    app.run()