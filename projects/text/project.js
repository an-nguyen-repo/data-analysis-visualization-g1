window.G1.projects.push({
  id: "text",
  type: "Text",
  title: "Tiêu đề bài Text (dummy)",
  summary: "Một câu tóm tắt giả cho bài dữ liệu văn bản, dài khoảng hai dòng trên thẻ.",
  problem:
    "Đoạn mô tả giả dùng để kiểm tra bố cục. Nội dung thật sẽ trình bày bối cảnh bài toán, câu hỏi cần trả lời, " +
    "thước đo đánh giá và lý do chọn cách tiếp cận. Câu này được viết đủ dài để xem cách chữ xuống dòng trong khung.",
  dataset: {
    name: "Bộ dữ liệu văn bản (dummy)",
    url: "https://example.com/dataset",
    samples: "16 000 mẫu: train / validation / test (dummy)",
    features: "Cột A, cột B, cột C, nhãn (dummy)",
    description: "Mô tả giả của bộ dữ liệu: nguồn gốc, giấy phép, các vấn đề chất lượng chính và cách nhóm xử lý.",
  },
  workflow: [
    { title: "Tải và kiểm tra dữ liệu", detail: "Mô tả giả cho bước này, một đến hai câu ngắn." },
    { title: "Phân tích khám phá", detail: "Mô tả giả cho bước này, một đến hai câu ngắn." },
    { title: "Tiền xử lý", detail: "Mô tả giả cho bước này, một đến hai câu ngắn." },
    { title: "Mô hình hoá", detail: "Mô tả giả cho bước này, một đến hai câu ngắn." },
    { title: "Đánh giá", detail: "Mô tả giả cho bước này, một đến hai câu ngắn." },
  ],
  owners: ["Nguyễn Thị Thu An"],
  status: "in-progress",
  links: { notebook: "projects/text/text.ipynb", report: null, video: null },
  results: [
    { model: "Baseline", metric: "Macro-F1 (test)", value: "0.40" },
    { model: "Mô hình A", metric: "Macro-F1 (test)", value: "0.65" },
    { model: "Mô hình B", metric: "Macro-F1 (test)", value: "0.72", final: true },
    { model: "Mô hình B", metric: "Accuracy (test)", value: "0.81", final: true },
  ],
  questions: [
    { q: "Câu hỏi phân tích thứ nhất?", a: "Câu trả lời giả kèm số liệu so sánh, ví dụ 0.65 so với 0.72." },
    { q: "Câu hỏi phân tích thứ hai?", a: "Câu trả lời giả kèm số liệu so sánh, ví dụ 0.65 so với 0.72." },
    { q: "Câu hỏi phân tích thứ ba?", a: "Câu trả lời giả kèm số liệu so sánh, ví dụ 0.65 so với 0.72." },
  ],
});
