import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class VRPTW_ACO:
    def __init__(self):
        # Thông số ACO
        self.alpha = 1.0  # Độ quan trọng của pheromone
        self.beta = 2.0   # Độ quan trọng của khoảng cách
        self.evaporation = 0.1  # Tốc độ bay hơi pheromone
        self.n_ants = 10  # Số lượng kiến
        self.max_iterations = 100  # Số vòng lặp tối đa
        
        # Khởi tạo cửa sổ
        self.window = tk.Tk()
        self.window.title("Giải bài toán VRPTW bằng ACO")
        self.create_gui()
        
    def create_gui(self):
        # Frame nhập liệu
        input_frame = ttk.LabelFrame(self.window, text="Thông số đầu vào")
        input_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Các trường nhập liệu
        ttk.Label(input_frame, text="Số khách hàng:").grid(row=0, column=0)
        self.n_customers = ttk.Entry(input_frame)
        self.n_customers.grid(row=0, column=1)
        
        ttk.Label(input_frame, text="Số xe:").grid(row=1, column=0)
        self.n_vehicles = ttk.Entry(input_frame)
        self.n_vehicles.grid(row=1, column=1)
        
        ttk.Label(input_frame, text="Sức chứa xe:").grid(row=2, column=0)
        self.vehicle_capacity = ttk.Entry(input_frame)
        self.vehicle_capacity.grid(row=2, column=1)
        
        ttk.Button(input_frame, text="Giải bài toán", command=self.solve).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame kết quả
        result_frame = ttk.LabelFrame(self.window, text="Kết quả")
        result_frame.grid(row=0, column=1, padx=10, pady=10)
        
        self.fig = plt.Figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack()
        
    def generate_data(self, n_customers):
        # Tạo dữ liệu mẫu
        self.depot = np.array([50, 50])  # Vị trí kho trung tâm
        self.locations = np.random.rand(n_customers, 2) * 100  # Vị trí khách hàng
        self.demands = np.random.randint(10, 30, size=n_customers)  # Nhu cầu khách hàng
        
        # Tạo time windows
        self.time_windows = []
        for _ in range(n_customers):
            ready_time = np.random.randint(0, 50)
            due_time = ready_time + np.random.randint(20, 50)
            service_time = np.random.randint(5, 15)
            self.time_windows.append((ready_time, due_time, service_time))
            
    def calculate_distance(self, point1, point2):
        return np.sqrt(np.sum((point1 - point2) ** 2))
    
    def run_aco(self):
        n_customers = len(self.locations)
        pheromone = np.ones((n_customers + 1, n_customers + 1))  # +1 cho depot
        best_solution = None
        best_cost = float('inf')
        
        for iteration in range(self.max_iterations):
            # Mỗi con kiến tìm đường
            for ant in range(self.n_ants):
                current_solution = self.construct_solution(pheromone)
                cost = self.calculate_solution_cost(current_solution)
                
                if cost < best_cost:
                    best_cost = cost
                    best_solution = current_solution.copy()
            
            # Cập nhật pheromone
            pheromone *= (1 - self.evaporation)
            self.update_pheromone(pheromone, best_solution, best_cost)
        
        return best_solution, best_cost
    
    def construct_solution(self, pheromone):
        # Xây dựng lời giải cho một con kiến
        # (Code chi tiết sẽ được thêm vào đây)
        return []
    
    def calculate_solution_cost(self, solution):
        # Tính tổng chi phí của lời giải
        # (Code chi tiết sẽ được thêm vào đây)
        return 0
    
    def update_pheromone(self, pheromone, solution, cost):
        # Cập nhật pheromone trên các cạnh
        # (Code chi tiết sẽ được thêm vào đây)
        pass
    
    def solve(self):
        try:
            n_customers = int(self.n_customers.get())
            n_vehicles = int(self.n_vehicles.get())
            vehicle_capacity = float(self.vehicle_capacity.get())
            
            # Tạo dữ liệu
            self.generate_data(n_customers)
            
            # Chạy thuật toán ACO
            best_routes, best_cost = self.run_aco()
            
            # Hiển thị kết quả
            self.display_results(best_routes, best_cost)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
    
    def display_results(self, routes, cost):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Vẽ depot
        ax.scatter([self.depot[0]], [self.depot[1]], c='red', marker='s', s=100, label='Kho')
        
        # Vẽ khách hàng
        ax.scatter(self.locations[:,0], self.locations[:,1], c='blue', label='Khách hàng')
        
        # Vẽ tuyến đường
        colors = plt.cm.rainbow(np.linspace(0, 1, len(routes)))
        for route, color in zip(routes, colors):
            points = np.vstack([self.depot, *[self.locations[i] for i in route], self.depot])
            ax.plot(points[:,0], points[:,1], c=color)
        
        ax.set_title(f'Tổng chi phí: {cost:.2f}')
        ax.legend()
        self.canvas.draw()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = VRPTW_ACO()
    app.run()