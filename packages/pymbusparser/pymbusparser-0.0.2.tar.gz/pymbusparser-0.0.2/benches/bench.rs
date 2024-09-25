use criterion::{black_box, criterion_group, criterion_main, Criterion};
use m_bus_parser::frames::Frame;

fn frame_parse_benchmark(c: &mut Criterion) {
    let data = vec![0x68, 0x04, 0x04, 0x68, 0x53, 0x01, 0x00, 0x00, 0x54, 0x16];
    c.bench_function("parse_frame_only", |b| {
        b.iter(|| {
            // Use black_box to prevent compiler optimizations from skipping the computation
            Frame::try_from(black_box(data.as_slice())).unwrap();
        })
    });
}

fn m_bus_parser_benchmark(c: &mut Criterion) {
    let data = vec![
        0x68, 0x3C, 0x3C, 0x68, 0x08, 0x08, 0x72, 0x78, 0x03, 0x49, 0x11, 0x77, 0x04, 0x0E, 0x16,
        0x0A, 0x00, 0x00, 0x00, 0x0C, 0x78, 0x78, 0x03, 0x49, 0x11, 0x04, 0x13, 0x31, 0xD4, 0x00,
        0x00, 0x42, 0x6C, 0x00, 0x00, 0x44, 0x13, 0x00, 0x00, 0x00, 0x00, 0x04, 0x6D, 0x0B, 0x0B,
        0xCD, 0x13, 0x02, 0x27, 0x00, 0x00, 0x09, 0xFD, 0x0E, 0x02, 0x09, 0xFD, 0x0F, 0x06, 0x0F,
        0x00, 0x01, 0x75, 0x13, 0xD3, 0x16,
    ];
    c.bench_function("parse", |b| {
        b.iter(|| {
            m_bus_parser::MbusData::try_from(data.as_slice()).unwrap();
        })
    });
}

criterion_group!(benches, frame_parse_benchmark, m_bus_parser_benchmark);
criterion_main!(benches);
