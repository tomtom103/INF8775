#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <deque>
#include <iostream>
#include <iterator>
#include <list>
#include <mutex>
#include <random>
#include <set>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <fstream>
#include <random>
#include <omp.h>

using namespace std;

class Enclosure {
public:
    // Add the default constructor
    Enclosure() : id(0), size(0) {}

    Enclosure(int _id, int _size) {
        id = _id;
        size = _size;
    }
    int id;
    int size;
    vector<pair<int, int>> shape;

    bool operator==(const Enclosure& other) const {
        return id == other.id && size == other.size && shape == other.shape;
    }

    struct Hash {
        size_t operator()(const Enclosure& enclosure) const {
            return hash<int>()(enclosure.id) ^ hash<int>()(enclosure.size);
        }
    };
};

vector<Enclosure> best_order;
mutex best_order_mutex;
vector<vector<int>> enclosure_weights;
mutex enclosure_weights_mutex;
bool print_path = false;

size_t hash_enclosures(const vector<Enclosure>& enclosures) {
    size_t seed = enclosures.size();
    for (const auto& enclosure : enclosures) {
        seed ^= enclosure.id + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    }
    return seed;
}

vector<vector<pair<int, int>>> generate_spiral_grid(const vector<Enclosure>& enclosures) {
    vector<pair<int, int>> sizes;
    for (const auto& enclosure : enclosures) {
        sizes.emplace_back(enclosure.id, enclosure.size);
    }

    vector<int> unrolled_enclosures;
    for (const auto& [id, size] : sizes) {
        unrolled_enclosures.insert(unrolled_enclosures.end(), size, id);
    }

    int n = unrolled_enclosures.size();
    int rows = ceil(sqrt(n));
    int cols = rows;

    vector<vector<pair<int, int>>> solution(enclosures.size());

    int row = rows / 2;
    int col = cols / 2;

    vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    int direction_index = 0;
    int steps_in_current_direction = 1;
    int steps_taken = 0;

    set<pair<int, int>> visited;

    for (int id : unrolled_enclosures) {
        solution[id].emplace_back(row, col);
        visited.insert(make_pair(row, col));

        if (steps_taken == steps_in_current_direction) {
            direction_index = (direction_index + 1) % 4;
            steps_taken = 0;
            if (direction_index == 0 || direction_index == 2) {
                steps_in_current_direction++;
            }
        }

        int next_row = row + directions[direction_index].first;
        int next_col = col + directions[direction_index].second;

        while (next_row < 0 || next_row >= rows || next_col < 0 || next_col >= cols || visited.count(make_pair(next_row, next_col))) {
            direction_index = (direction_index + 1) % 4;
            next_row = row + directions[direction_index].first;
            next_col = col + directions[direction_index].second;
            if (direction_index == 0 || direction_index == 2) {
                steps_in_current_direction++;
            }
        }

        row = next_row;
        col = next_col;
        steps_taken++;
    }

    return solution;
}


vector<Enclosure> swap_random_enclosures(vector<Enclosure>& enclosures, int neighborhood_type, unordered_set<size_t>& tabu_set, size_t max_tabu_size) {
    mt19937 gen(random_device{}());

    vector<Enclosure> new_solution;

    size_t new_hash;
    do {
        new_solution = enclosures;
        if (neighborhood_type == 0) {  // Single enclosure swap
            uniform_int_distribution<> swap_dist(0, enclosures.size() - 1);
            int idx1 = swap_dist(gen);
            int idx2 = swap_dist(gen);

            swap(new_solution[idx1], new_solution[idx2]);

        } else if (neighborhood_type == 1) {  // Adjacent enclosures swap
            uniform_int_distribution<> swap_dist(0, enclosures.size() - 2);
            int idx1 = swap_dist(gen);

            swap(new_solution[idx1], new_solution[idx1 + 1]);

        } else if (neighborhood_type == 2) {  // Swapping pairs of enclosures
            uniform_int_distribution<> swap_dist(0, enclosures.size() - 2);
            int idx1 = swap_dist(gen);
            int idx2 = swap_dist(gen);

            swap(new_solution[idx1], new_solution[idx2]);
            swap(new_solution[idx1 + 1], new_solution[idx2 + 1]);

        } else if (neighborhood_type == 3) {  // Reversing subsequence of enclosures
            uniform_int_distribution<> start_dist(0, enclosures.size() - 2);
            int start = start_dist(gen);
            uniform_int_distribution<> length_dist(2, enclosures.size() - start);
            int length = length_dist(gen);

            reverse(new_solution.begin() + start, new_solution.begin() + start + length);
        }
        new_hash = hash_enclosures(new_solution);
    } while (tabu_set.count(new_hash) > 0);

    // Update the tabu list
    if (tabu_set.size() >= max_tabu_size) {
        tabu_set.erase(tabu_set.begin());
    }
    tabu_set.insert(new_hash);

    return new_solution;
}

inline int distance(int x1, int y1, int x2, int y2) {
    return abs(x2 - x1) + abs(y2 - y1);
}

long long total_score(const vector<vector<pair<int, int>>>& solution, const vector<vector<int>>& weights, const vector<int>& bonus_enclosures, int k) {
    vector<vector<int>> distances(solution.size(), vector<int>(solution.size(), 99999));

    #pragma omp parallel for
    for (size_t zero = 0; zero < solution.size(); ++zero) {
        for (size_t one = zero + 1; one < solution.size(); ++one) {
            for (const auto& [x_start, y_start] : solution[zero]) {
                for (const auto& [x_end, y_end] : solution[one]) {
                    int length = distance(x_start, y_start, x_end, y_end);
                    #pragma omp critical
                    {
                        if (length < distances[zero][one]) {
                            distances[zero][one] = length;
                            distances[one][zero] = length;
                        }
                    }
                }
            }
        }
    }

    long long sum = 0;
    for (size_t i = 0; i < solution.size(); ++i) {
        for (size_t j = 0; j < solution.size(); ++j) {
            sum += weights[i][j] * distances[i][j];
        }
    }

    long long bonus = pow(bonus_enclosures.size(), 2);
    for (size_t i = 0; i < bonus_enclosures.size(); ++i) {
        for (size_t j = i + 1; j < bonus_enclosures.size(); ++j) {
            if (distances[bonus_enclosures[i]][bonus_enclosures[j]] > k) {
                bonus = 0;
                break;
            }
        }
        if (bonus == 0) {
            break;
        }
    }

    return bonus - sum;
}

pair<vector<Enclosure>, long long> late_acceptance_hill_climbing(
    vector<Enclosure> enclosures,
    vector<int> bonus_enclosures,
    vector<vector<int>> weights,
    int k,
    int look_back_steps,
    int max_iterations
) {
    int num_threads = thread::hardware_concurrency();
    if (num_threads == 0) {
        num_threads = 4; // Default number of threads
    }
    // vector<thread> threads(num_threads);
    vector<pair<vector<Enclosure>, int>> results(num_threads);

    # pragma omp parallel for
    for (int i = 0; i < num_threads; ++i) {
        // threads[i] = thread([&results, i, &enclosures, &bonus_enclosures, &weights, k, look_back_steps, max_iterations]() {
        vector<Enclosure> new_best_order = enclosures;
        long long best_score = total_score(generate_spiral_grid(enclosures), weights, bonus_enclosures, k);

        vector<Enclosure> current_solution = enclosures;
        long long current_score = best_score;

        vector<long long> scores_history(look_back_steps, current_score);

        unordered_set<size_t> tabu_set;
        int max_tabu_size = 10;

        for (int iteration = 0; iteration < max_iterations; ++iteration) {
            int neighborhood_type = iteration % 4;
            vector<Enclosure> new_solution = swap_random_enclosures(current_solution, neighborhood_type, tabu_set, max_tabu_size);
            long long new_score = total_score(generate_spiral_grid(new_solution), weights, bonus_enclosures, k);

            int history_index = iteration % look_back_steps;
            if (new_score >= scores_history[history_index]) {
                current_solution = new_solution;
                current_score = new_score;
                scores_history[history_index] = new_score;
            }

            if (current_score > best_score) {
                new_best_order = current_solution;
                best_score = current_score;
            }
        }
        # pragma omp critical
        {
            results[i] = make_pair(new_best_order, best_score);
        }
    }

    return *max_element(results.begin(), results.end(), [](const auto& lhs, const auto& rhs) {
        return lhs.second < rhs.second;
    });
}


void print_solution(const vector<vector<pair<int, int>>>& solution) {
    for (const auto& coordinates : solution) {
        for (const auto& [x, y] : coordinates) {
            cout << x << " " << y << " ";
        }
        cout << endl;
        }
    cout << endl;
}

void read_file(const string& file_path, int& n, int& m, int& k, vector<int>& bonus_enclosures, vector<int>& enclosure_sizes, vector<vector<int>>& enclosure_weights) {
    ifstream file(file_path);
    if (!file.is_open()) {
        throw runtime_error("Error: Unable to open the file.");
    }

    file >> n >> m >> k;

    bonus_enclosures.resize(m);
    for (int i = 0; i < m; ++i) {
        file >> bonus_enclosures[i];
    }

    enclosure_sizes.resize(n);
    for (int i = 0; i < n; ++i) {
        file >> enclosure_sizes[i];
    }

    enclosure_weights.resize(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file >> enclosure_weights[i][j];
        }
    }
}


int main(int argc, char* argv[]) {
    thread timer([]() {
        this_thread::sleep_for(chrono::seconds(120));
        exit(0);
    });
    timer.detach();

    string input_file_path;
    bool p = false;

    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];

        if (arg == "-e") {
            if (i + 1 < argc) {
                input_file_path = argv[++i];
            } else {
                cerr << "Error: -e option requires an argument." << endl;
                return 1;
            }
        } else if (arg == "-p") {
            p = true;
        } else {
            cerr << "Error: Unknown option '" << arg << "'." << endl;
            return 1;
        }
    }

    if (input_file_path.empty()) {
        cerr << "Error: -e option is required." << endl;
        return 1;
    }

    int n, m, k;
    vector<int> bonus_enclosures;
    vector<int> enclosure_sizes;
    vector<vector<int>> enclosure_weights;

    read_file(input_file_path, n, m, k, bonus_enclosures, enclosure_sizes, enclosure_weights);

    vector<Enclosure> enclosures;

    for(int i = 0; i < n; ++i) {
        enclosures.push_back(Enclosure(i, enclosure_sizes[i]));
    }

    auto best_order = enclosures;
    auto solution = generate_spiral_grid(best_order);
    long long best_score = total_score(solution, enclosure_weights, bonus_enclosures, k);

    if(p) {
        print_solution(solution);
    } else {
        cout << best_score << endl;
    }

    while (true) {
        auto [new_order, new_score] = late_acceptance_hill_climbing(best_order, bonus_enclosures, enclosure_weights, k, 500, 1000);
        if (new_score > best_score) {
            unique_lock<mutex> lock(best_order_mutex);
            best_order = new_order;
            best_score = new_score;
            if (p) {
                solution = generate_spiral_grid(best_order);
                print_solution(solution);
            } else {
                cout << best_score << endl;
            }
        }
    }

    return 0;
}
