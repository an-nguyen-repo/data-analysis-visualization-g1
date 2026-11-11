window.G1.projects.push({
  id: "tabular",
  type: "Tabular",
  title: "Tiêu đề bài Tabular (dummy)",
  summary: "Một câu tóm tắt giả cho bài dữ liệu dạng bảng, dài khoảng hai dòng trên thẻ.",
  problem:
    "Đoạn mô tả giả dùng để kiểm tra bố cục. Nội dung thật sẽ trình bày bối cảnh bài toán, câu hỏi cần trả lời, " +
    "thước đo đánh giá và lý do chọn cách tiếp cận. Câu này được viết đủ dài để xem cách chữ xuống dòng trong khung.",
  dataset: {
    name: "Bộ dữ liệu bảng (dummy)",
    url: "https://example.com/dataset",
    samples: "10 000 mẫu: train / validation / test (dummy)",
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
  owners: ["Phan Thị Minh Thơ"],
  status: "planned",
  links: { notebook: null, report: null, video: null },
  results: null,
  questions: null,
});
