import random

# Khởi tạo các thông số ban đầu
so_kien = 10
so_thanh_pho = int(input("Nhập số thành phố: "))
alpha = 1.0  # Độ quan trọng của pheromone
beta = 2.0   # Độ quan trọng của khoảng cách
bay_hoi = 0.1  # Tốc độ bay hơi pheromone
max_vong = 100  # Số vòng lặp tối đa

# Nhập ma trận khoảng cách
print("Nhập ma trận khoảng cách giữa các thành phố:")
khoang_cach = []
for i in range(so_thanh_pho):
    hang = []
    for j in range(so_thanh_pho):
        if i == j:
            hang.append(0)
        elif j > i:
            kc = float(input(f"Nhập khoảng cách từ thành phố {i} đến thành phố {j}: "))
            hang.append(kc)
        else:
            hang.append(khoang_cach[j][i])
    khoang_cach.append(hang)

# In ma trận khoảng cách
print("\nMa trận khoảng cách đã nhập:")
for hang in khoang_cach:
    print(hang)

# Khởi tạo ma trận pheromone
pheromone = []
for i in range(so_thanh_pho):
    hang = []
    for j in range(so_thanh_pho):
        hang.append(1.0)  # Giá trị pheromone ban đầu = 1
    pheromone.append(hang)

# Bắt đầu thuật toán
duong_di_tot_nhat = None
do_dai_tot_nhat = float('inf')

for vong in range(max_vong):
    # Mỗi con kiến sẽ tìm đường đi
    for kien in range(so_kien):
        thanh_pho_hien_tai = random.randint(0, so_thanh_pho - 1)
        thanh_pho_da_di = [thanh_pho_hien_tai]
        do_dai_duong_di = 0
        
        # Tìm đường đi qua tất cả thành phố
        while len(thanh_pho_da_di) < so_thanh_pho:
            # Tính xác suất chọn thành phố tiếp theo
            xac_suat = []
            tong_xac_suat = 0
            
            for tp in range(so_thanh_pho):
                if tp not in thanh_pho_da_di:
                    tau = pheromone[thanh_pho_hien_tai][tp] ** alpha
                    eta = (1.0 / khoang_cach[thanh_pho_hien_tai][tp]) ** beta
                    xac_suat.append([tp, tau * eta])
                    tong_xac_suat += tau * eta
            
            # Chuẩn hóa xác suất
            for i in range(len(xac_suat)):
                xac_suat[i][1] /= tong_xac_suat
            
            # Chọn thành phố tiếp theo
            r = random.random()
            tong = 0
            for tp, p in xac_suat:
                tong += p
                if r <= tong:
                    thanh_pho_da_di.append(tp)
                    do_dai_duong_di += khoang_cach[thanh_pho_hien_tai][tp]
                    thanh_pho_hien_tai = tp
                    break
        
        # Cập nhật đường đi tốt nhất
        if do_dai_duong_di < do_dai_tot_nhat:
            do_dai_tot_nhat = do_dai_duong_di
            duong_di_tot_nhat = thanh_pho_da_di.copy()
    
    # Bay hơi pheromone
    for i in range(so_thanh_pho):
        for j in range(so_thanh_pho):
            pheromone[i][j] *= (1 - bay_hoi)
    
    # Cập nhật pheromone trên đường đi tốt nhất
    for i in range(len(duong_di_tot_nhat) - 1):
        tp1 = duong_di_tot_nhat[i]
        tp2 = duong_di_tot_nhat[i + 1]
        pheromone[tp1][tp2] += 1.0 / do_dai_tot_nhat
        pheromone[tp2][tp1] += 1.0 / do_dai_tot_nhat

print("Đường đi tốt nhất:", duong_di_tot_nhat)
print("Độ dài đường đi:", do_dai_tot_nhat)