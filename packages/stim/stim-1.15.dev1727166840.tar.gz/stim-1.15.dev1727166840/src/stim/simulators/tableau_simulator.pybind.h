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

#ifndef _STIM_SIMULATORS_TABLEAU_SIMULATOR_PYBIND_H
#define _STIM_SIMULATORS_TABLEAU_SIMULATOR_PYBIND_H

#include <pybind11/pybind11.h>

#include "stim/simulators/tableau_simulator.h"

namespace stim_pybind {

pybind11::class_<stim::TableauSimulator<stim::MAX_BITWORD_WIDTH>> pybind_tableau_simulator(pybind11::module &m);
void pybind_tableau_simulator_methods(
    pybind11::module &m, pybind11::class_<stim::TableauSimulator<stim::MAX_BITWORD_WIDTH>> &c);

}  // namespace stim_pybind

#endif
