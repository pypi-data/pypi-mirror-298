// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "stim/cmd/command_sample.h"

#include "command_help.h"
#include "stim/io/stim_data_formats.h"
#include "stim/simulators/frame_simulator.h"
#include "stim/simulators/frame_simulator_util.h"
#include "stim/simulators/tableau_simulator.h"
#include "stim/util_bot/arg_parse.h"
#include "stim/util_bot/probability_util.h"

using namespace stim;

int stim::command_sample(int argc, const char **argv) {
    check_for_unknown_arguments(
        {"--seed", "--skip_reference_sample", "--out_format", "--out", "--in", "--shots"},
        {"--sample", "--frame0"},
        "sample",
        argc,
        argv);
    const auto &out_format = find_enum_argument("--out_format", "01", format_name_to_enum_map(), argc, argv);
    bool skip_reference_sample = find_bool_argument("--skip_reference_sample", argc, argv);
    uint64_t num_shots =
        find_argument("--shots", argc, argv)    ? (uint64_t)find_int64_argument("--shots", 1, 0, INT64_MAX, argc, argv)
        : find_argument("--sample", argc, argv) ? (uint64_t)find_int64_argument("--sample", 1, 0, INT64_MAX, argc, argv)
                                                : 1;
    if (num_shots == 0) {
        return EXIT_SUCCESS;
    }
    FILE *in = find_open_file_argument("--in", stdin, "rb", argc, argv);
    FILE *out = find_open_file_argument("--out", stdout, "wb", argc, argv);
    auto rng = optionally_seeded_rng(argc, argv);
    bool deprecated_frame0 = find_bool_argument("--frame0", argc, argv);
    if (deprecated_frame0) {
        std::cerr << "[DEPRECATION] Use `--skip_reference_sample` instead of `--frame0`\n";
        skip_reference_sample = true;
    }

    if (num_shots == 1 && !skip_reference_sample) {
        TableauSimulator<MAX_BITWORD_WIDTH>::sample_stream(in, out, out_format.id, false, rng);
    } else {
        assert(num_shots > 0);
        auto circuit = Circuit::from_file(in);
        simd_bits<MAX_BITWORD_WIDTH> ref(0);
        if (!skip_reference_sample) {
            ref = TableauSimulator<MAX_BITWORD_WIDTH>::reference_sample_circuit(circuit);
        }
        sample_batch_measurements_writing_results_to_disk(circuit, ref, num_shots, out, out_format.id, rng);
    }

    if (in != stdin) {
        fclose(in);
    }
    if (out != stdout) {
        fclose(out);
    }
    return EXIT_SUCCESS;
}

SubCommandHelp stim::command_sample_help() {
    SubCommandHelp result;
    result.subcommand_name = "sample";
    result.description = "Samples measurements from a circuit.";

    result.examples.push_back(clean_doc_string(R"PARAGRAPH(
            >>> cat example_circuit.stim
            H 0
            CNOT 0 1
            M 0 1

            >>> stim sample --shots 5 < example_circuit.stim
            00
            11
            11
            00
            11

        )PARAGRAPH"));
    result.examples.push_back(clean_doc_string(R"PARAGRAPH(
            >>> cat example_circuit.stim
            X 2 3 5
            M 0 1 2 3 4 5 6 7 8 9

            >>> stim sample --in example_circuit.stim --out_format dets
            shot M2 M3 M5
        )PARAGRAPH"));

    result.flags.push_back(SubCommandHelpFlag{
        "--skip_reference_sample",
        "bool",
        "false",
        {"[none]", "[switch]"},
        clean_doc_string(R"PARAGRAPH(
            Asserts the circuit can produce a noiseless sample that is just 0s.

            When this argument is specified, the reference sample (that is used
            to convert measurement flip data from frame simulations into actual
            measurement data) is generated by simply setting all measurements to
            0 instead of by performing a stabilizer tableau simulation of the
            circuit without noise.

            Skipping the reference sample can significantly improve performance,
            because acquiring the reference sample requires using the tableau
            simulator. If the vacuous reference sample is actually a result that
            can be produced by the circuit, under noiseless execution, then
            specifying this flag has no observable outcome other than improving
            performance.

            CAUTION. When the all-zero sample isn't a result that can be
            produced by the circuit under noiseless execution, specifying this
            flag will cause incorrect output to be produced. Specifically, the
            output measurement bits will be whether each measurement was
            *FLIPPED* instead of the actual absolute value of the measurement.
        )PARAGRAPH"),
    });

    result.flags.push_back(SubCommandHelpFlag{
        "--out_format",
        "01|b8|r8|ptb64|hits|dets",
        "01",
        {"[none]", "format"},
        clean_doc_string(R"PARAGRAPH(
            Specifies the data format to use when writing output data.

            The available formats are:

                01 (default): dense human readable
                b8: bit packed binary
                r8: run length binary
                ptb64: partially transposed bit packed binary for SIMD
                hits: sparse human readable
                dets: sparse human readable with type hints

            For a detailed description of each result format, see the result
            format reference:
            https://github.com/quantumlib/Stim/blob/main/doc/result_formats.md
        )PARAGRAPH"),
    });

    result.flags.push_back(SubCommandHelpFlag{
        "--seed",
        "int",
        "system_entropy",
        {"[none]", "int"},
        clean_doc_string(R"PARAGRAPH(
            Makes simulation results PARTIALLY deterministic.

            The seed integer must be a non-negative 64 bit signed integer.

            When `--seed` isn't specified, the random number generator is seeded
            using fresh entropy requested from the operating system.

            When `--seed #` is set, the exact same simulation results will be
            produced every time ASSUMING:

            - the exact same other flags are specified
            - the exact same version of Stim is being used
            - the exact same machine architecture is being used (for example,
                you're not switching from a machine that has AVX2 instructions
                to one that doesn't).

            CAUTION: simulation results *WILL NOT* be consistent between
            versions of Stim. This restriction is present to make it possible to
            have future optimizations to the random sampling, and is enforced by
            introducing intentional differences in the seeding strategy from
            version to version.

            CAUTION: simulation results *MAY NOT* be consistent across machines.
            For example, using the same seed on a machine that supports AVX
            instructions and one that only supports SSE instructions may produce
            different simulation results.

            CAUTION: simulation results *MAY NOT* be consistent if you vary
            other flags and modes. For example, `--skip_reference_sample` may
            result in fewer calls the to the random number generator before
            reported sampling begins. More generally, using the same seed for
            `stim sample` and `stim detect` will not result in detection events
            corresponding to the measurement results.
        )PARAGRAPH"),
    });

    result.flags.push_back(SubCommandHelpFlag{
        "--shots",
        "int",
        "1",
        {"[none]", "int"},
        clean_doc_string(R"PARAGRAPH(
            Specifies the number of samples to take from the circuit.

            Defaults to 1.
            Must be an integer between 0 and a quintillion (10^18).
        )PARAGRAPH"),
    });

    result.flags.push_back(SubCommandHelpFlag{
        "--in",
        "filepath",
        "{stdin}",
        {"[none]", "filepath"},
        clean_doc_string(R"PARAGRAPH(
            Chooses the stim circuit file to read the circuit to sample from.

            By default, the circuit is read from stdin. When `--in $FILEPATH` is
            specified, the circuit is instead read from the file at $FILEPATH.

            The input should be a stim circuit. See:
            https://github.com/quantumlib/Stim/blob/main/doc/file_format_stim_circuit.md
        )PARAGRAPH"),
    });

    result.flags.push_back(SubCommandHelpFlag{
        "--out",
        "filepath",
        "{stdout}",
        {"[none]", "filepath"},
        clean_doc_string(R"PARAGRAPH(
            Chooses where to write the sampled data to.

            By default, the output is written to stdout. When `--out $FILEPATH`
            is specified, the output is instead written to the file at $FILEPATH.

            The output is in a format specified by `--out_format`. See:
            https://github.com/quantumlib/Stim/blob/main/doc/result_formats.md
        )PARAGRAPH"),
    });

    return result;
}
