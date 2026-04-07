# Test Results – TravelBuddy AI Agent

> Ghi lại kết quả chạy thực tế từ `python main.py`

---

## Test 1 – Direct Answer (Không cần tool)

**Input:**
```
Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Chào bạn! Tuyệt vời quá! Bạn đã có ý tưởng nào về địa điểm hay thời gian đi chưa? Hoặc nếu bạn muốn, mình có thể giúp bạn gợi ý một số điểm đến thú vị tại Việt Nam. Bạn thích đi biển, núi, hay tham quan thành phố? Chia sẻ với mình nhé!
```

**Kết quả:** ✅ PASS – Agent chào hỏi và hỏi thêm thông tin, không gọi tool.

---

## Test 2 – Single Tool Call

**Input:**
```
Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
[Tool] search_flights: Hà Nội -> Đà Nẵng
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: ✈️ Chuyến bay từ Hà Nội đi Đà Nẵng có các lựa chọn như sau:

1. **Vietnam Airlines** | 06:00 → 07:20 | 1.450.000đ | Phổ thông
2. **Vietnam Airlines** | 14:00 → 15:20 | 2.800.000đ | Thương gia
3. **VietJet Air** | 08:30 → 09:50 | 890.000đ | Phổ thông
4. **Bamboo Airways** | 11:00 → 12:20 | 1.200.000đ | Phổ thông

Bạn có muốn tìm khách sạn tại Đà Nẵng không? Nếu có ngân sách hoặc yêu cầu cụ thể nào, hãy cho mình biết nhé!
```

**Kết quả:** ✅ PASS – Agent gọi đúng 1 tool, liệt kê đủ 4 chuyến bay.

---

## Test 3 – Multi-Step Tool Chaining

**Input:**
```
Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
[Tool] search_flights: Hà Nội -> Phú Quốc
  → Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1500000})
[Tool] search_hotels: Phú Quốc, giá tối đa 1.500.000đ/đêm
  → Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1350000,khách_sạn:3200000'})
[Tool] calculate_budget: ngân sách 5.000.000đ, chi phí: vé_máy_bay:1350000,khách_sạn:3200000
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Dưới đây là kế hoạch chuyến đi của bạn từ Hà Nội đến Phú Quốc:

✈️ **Chuyến bay:**  
- **Hãng:** VietJet Air  
- **Giờ bay:** 10:00 → 12:15  
- **Giá vé:** 1.350.000đ  

🏨 **Khách sạn:**  
- **Tên:** Lahana Resort ★★★  
- **Giá/đêm:** 800.000đ  
- **Thời gian lưu trú:** 2 đêm (1.600.000đ)  
- **Khu vực:** Dương Đông  
- **Rating:** 4.0/5  

💰 **Tổng chi phí ước tính:**  
- **Vé máy bay:** 1.350.000đ  
- **Khách sạn:** 1.600.000đ  
---
- **Tổng chi:** 2.950.000đ  
- **Ngân sách:** 5.000.000đ  
- **Còn lại:** 2.050.000đ  

💡 **Gợi ý thêm:** 
- Với số tiền còn lại, bạn có thể chi tiêu cho ẩm thực và tham quan. Phú Quốc nổi tiếng với món cá nướng, hải sản tươi sống, và các điểm tham quan như Vinpearl Land, Dinh Cậu, hay bãi Sao.

Nếu bạn cần thêm thông tin hoặc muốn điều chỉnh kế hoạch, hãy cho mình biết nhé!
```

**Kết quả:** ✅ PASS – Agent tự động chuỗi 3 tool calls, tổng hợp đầy đủ.

---

## Test 4 – Missing Info / Clarification

**Input:**
```
Tôi muốn đặt khách sạn
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Mình rất vui được giúp bạn! Bạn hãy cho mình biết thành phố mà bạn muốn đặt khách sạn nhé. Nếu bạn có ngân sách cụ thể, hãy nói rõ để mình có thể tìm kiếm phòng phù hợp.
```

**Kết quả:** ✅ PASS – Agent không gọi tool, chỉ hỏi lại thông tin cần thiết.

---

## Test 5 – Guardrail / Refusal

**Input:**
```
Giải giúp tôi bài tập lập trình Python về linked list
```

**Console log:**
```
TravelBuddy đang suy nghĩ...
  → Trả lời trực tiếp (không gọi tool)
```

**Output:**
```
TravelBuddy: Xin lỗi, nhưng tôi chỉ hỗ trợ về du lịch thôi. Nếu bạn cần tư vấn về một chuyến đi hoặc đặt phòng khách sạn, hãy cho tôi biết nhé!
```

**Kết quả:** ✅ PASS – Agent từ chối lịch sự và gợi ý quay lại chủ đề du lịch.
