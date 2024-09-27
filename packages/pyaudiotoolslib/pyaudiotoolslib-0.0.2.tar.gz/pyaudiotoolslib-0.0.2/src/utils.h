#pragma once

#include <cmath>

#define DB_TO_LINEAR(x) (std::pow(10.0, (x) / 20.0))
#define LINEAR_TO_DB(x) (20.0 * std::log10(x))