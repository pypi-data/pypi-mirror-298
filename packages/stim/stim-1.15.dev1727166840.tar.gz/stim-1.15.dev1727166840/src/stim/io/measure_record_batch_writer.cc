/*
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "stim/io/measure_record_batch_writer.h"

#include <algorithm>

using namespace stim;

MeasureRecordBatchWriter::MeasureRecordBatchWriter(FILE *out, size_t num_shots, SampleFormat output_format)
    : output_format(output_format), out(out) {
    if (num_shots > 768) {
        throw std::out_of_range("num_shots > 768 (safety check to ensure staying away from linux file handle limit)");
    }
    if (output_format == SampleFormat::SAMPLE_FORMAT_PTB64 && num_shots % 64 != 0) {
        throw std::out_of_range("Number of shots must be a multiple of 64 to use output format ptb64.");
    }
    auto f = output_format;
    auto s = num_shots;
    if (output_format == SampleFormat::SAMPLE_FORMAT_PTB64) {
        f = SampleFormat::SAMPLE_FORMAT_B8;
        s += 63;
        s /= 64;
    }
    if (s) {
        writers.push_back(MeasureRecordWriter::make(out, f));
    }
    for (size_t k = 1; k < s; k++) {
        FILE *file = tmpfile();
        if (file == nullptr) {
            throw std::out_of_range("Failed to open a temp file.");
        }
        writers.push_back(MeasureRecordWriter::make(file, f));
        temporary_files.push_back(file);
    }
}

MeasureRecordBatchWriter::~MeasureRecordBatchWriter() {
    for (auto &e : temporary_files) {
        fclose(e);
    }
    temporary_files.clear();
}

void MeasureRecordBatchWriter::begin_result_type(char result_type) {
    for (auto &e : writers) {
        e->begin_result_type(result_type);
    }
}

void MeasureRecordBatchWriter::write_end() {
    for (auto &writer : writers) {
        writer->write_end();
    }

    for (FILE *file : temporary_files) {
        rewind(file);
        while (true) {
            int c = getc(file);
            if (c == EOF) {
                break;
            }
            putc(c, out);
        }
        fclose(file);
    }
    temporary_files.clear();
}
