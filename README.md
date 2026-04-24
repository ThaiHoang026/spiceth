# SpiceTH

## Giới thiệu

SpiceTH là một project mô phỏng mạch điện đơn giản sử dụng phương pháp **Modified Nodal Analysis (MNA)**.
Chương trình hỗ trợ phân tích mạch ở chế độ **DC** và **AC**, với các phần tử cơ bản như R, L, C, các nguồn độc lập I, V các nguồn phụ thuộc.

---

## Cách chạy project

### 1. Yêu cầu

Đảm bảo bạn đã cài:

* Git
* Python (khuyến nghị Python ≥ 3.8)

---

### 2. Clone project

Mở terminal và chạy:

```bash
git clone https://github.com/ThaiHoang026/spiceth.git
cd spiceth
```

---

### 3. (Khuyến nghị) Tạo virtual environment

```bash
python -m venv venv
```

Kích hoạt:

* Windows:

```bash
venv\Scripts\activate
```

* macOS/Linux:

```bash
source venv/bin/activate
```

---

### 4. Nhập mạch vào file `netlist.cir`
(Có ví dụ trong file netlist.cir)

#### Cú pháp các phần tử:
**Điện trở, cuộn cảm, tụ điện (R, L, C):**
```
Name node1 node2 value
```

**Nguồn dòng, nguồn áp (I, V):**
```
Name node1 node2 DC dc_value AC ac_mag ac_phase
```

**Nguồn phụ thuộc dòng (F, H):**
```
Name node1 node2 Vctrl gain
```
* `Vctrl`: tên nguồn áp điều khiển

**Nguồn phụ thuộc áp (G, E):**
```
Name n1 n2 nc1 nc2 gain
```

---

### 5. Chọn chế độ phân tích

Mở file `main.py`, chỉnh một trong hai dòng sau:

**Phân tích DC:**

```python
G, b = MNABuilder(circuit).build_dc()
```

**Phân tích AC:**

```python
G, b = MNABuilder(circuit).build_ac()
```

---

### 6. Thiết lập tần số (chế độ AC)

Trong file `mna_builder.py`:

```python
f = 100  # Hz (tự chỉnh theo nhu cầu)
```

---

### 7. Chạy chương trình

```bash
cd src
python main.py
```

---

## Lưu ý

* Đảm bảo đang đứng đúng thư mục `src` khi chạy chương trình
* Kiểm tra lại netlist nếu kết quả không đúng (sai node là lỗi phổ biến)
* Nếu gặp lỗi module, kiểm tra lại môi trường Python

---

## Ghi chú

Project đang trong quá trình phát triển và có thể tồn tại lỗi.
Mọi đóng góp hoặc feedback đều được hoan nghênh
