#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

struct Edge {
    string u, v;
    int weight;
};

struct Graph {
    vector<string> vertices;
    vector<Edge> edges;
};

// Function to parse the input file
Graph loadInput(const string& filename) {
    Graph g;
    ifstream file(filename);
    string line, mode;

    while (getline(file, line)) {
        if (line.empty()) continue;
        if (line == "V" || line == "E") {
            mode = line;
            continue;
        }

        if (mode == "V") {
            // Remove parentheses
            line.erase(remove(line.begin(), line.end(), '('), line.end());
            line.erase(remove(line.begin(), line.end(), ')'), line.end());
            g.vertices.push_back(line);
        } else if (mode == "E") {
            stringstream ss(line);
            string u, v, w_str;
            getline(ss, u, '-');
            getline(ss, v, '-');
            getline(ss, w_str);

            // Clean up node names
            u.erase(remove(u.begin(), u.end(), '('), u.end());
            u.erase(remove(u.begin(), u.end(), ')'), u.end());
            v.erase(remove(v.begin(), v.end(), '('), v.end());
            v.erase(remove(v.begin(), v.end(), ')'), v.end());

            g.edges.push_back({u, v, stoi(w_str)});
        }
    }
    return g;
}

// Calculate the weight of the cut
long long checkEdge(const unordered_set<string>& S,
                    const unordered_set<string>& T, const vector<Edge>& edges) {
    long long sum = 0;
    for (const auto& edge : edges) {
        if ((S.count(edge.u) && T.count(edge.v)) ||
            (T.count(edge.u) && S.count(edge.v))) {
            sum += edge.weight;
        }
    }
    return sum;
}

// Local search: Try moving one node to the other set to improve the cut
long long checkNeighbors(unordered_set<string>& S, unordered_set<string>& T,
                         long long currentSolution, const vector<Edge>& edges) {
    long long bestLocalSolution = currentSolution;
    string bestNode = "";
    bool fromS = true;

    // Try moving nodes from S to T
    for (const string& node : S) {
        unordered_set<string> nextS = S;
        unordered_set<string> nextT = T;
        nextS.erase(node);
        nextT.insert(node);

        long long newSol = checkEdge(nextS, nextT, edges);
        if (newSol > bestLocalSolution) {
            bestLocalSolution = newSol;
            bestNode = node;
            fromS = true;
        }
    }

    // Try moving nodes from T to S
    for (const string& node : T) {
        unordered_set<string> nextS = S;
        unordered_set<string> nextT = T;
        nextT.erase(node);
        nextS.insert(node);

        long long newSol = checkEdge(nextS, nextT, edges);
        if (newSol > bestLocalSolution) {
            bestLocalSolution = newSol;
            bestNode = node;
            fromS = false;
        }
    }

    // Apply the best move found
    if (!bestNode.empty()) {
        if (fromS) {
            S.erase(bestNode);
            T.insert(bestNode);
        } else {
            T.erase(bestNode);
            S.insert(bestNode);
        }
    }

    return bestLocalSolution;
}

long long randomIteration(Graph& g, mt19937& rng) {
    vector<string> shuffledV = g.vertices;
    shuffle(shuffledV.begin(), shuffledV.end(), rng);

    unordered_set<string> S, T;
    for (int i = 0; i < shuffledV.size(); ++i) {
        if (i < 3)
            S.insert(shuffledV[i]);
        else
            T.insert(shuffledV[i]);
    }

    long long currentSolution = checkEdge(S, T, g.edges);
    bool improved = true;

    while (improved) {
        long long nextSolution = checkNeighbors(S, T, currentSolution, g.edges);
        if (nextSolution > currentSolution) {
            currentSolution = nextSolution;
        } else {
            improved = false;
        }
    }
    return currentSolution;
}

int main() {
    Graph g = loadInput("input_format");  // Ensure your filename matches
    if (g.vertices.empty()) {
        cout << "No vertices found. Check input file path/format." << endl;
        return 1;
    }

    random_device rd;
    mt19937 rng(rd());

    long long highestSolution = 0;

    cout << "Running 100 iterations..." << endl;
    for (int i = 0; i < 100; ++i) {
        long long sol = randomIteration(g, rng);
        if (sol > highestSolution) {
            highestSolution = sol;
        }
    }

    cout << "Highest Max-Cut found: " << highestSolution << endl;

    return 0;
}