#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <omp.h>
#include <time.h>

using namespace std;

// Declare global variables that functions can access (this way, we don't have to pass them as args)
string a;   // the line representation, which is a string on the alphabet, {H, G, W, T}
std::vector<std::vector<int> > opt_pairs_table;      // table for storing memoized outputs of OPT for all i and j pairs

int OPT(int i, int j){
    // Use memoized result, if available
    if (opt_pairs_table[i][j] != -1){
        return opt_pairs_table[i][j];
    }

    // To avoid sharp turns, we don't look for pairs when i and j are less than or equal to 4 spaces away from each other
    if (i >= (j-4)){
        opt_pairs_table[i][j] = 0;
        return 0;
    }

    // Set the max optimal number of pairs to opt_pairs_table[i][j-1], in case no optimal t is found that beats it
    // NOTE: Because this iterative algorithm is bottom up,
    // the table look-up below should have a memoized value already
    int max_opt = opt_pairs_table[i][j-1];

    // Look for optimal pairing for a[j] (which we call a[t]), by going through all possible t's
    for (int t = i; t < (j-4); t++){
        // check if valid pairing
        string pair = string() + a[t] + a[j];
        if ((pair == "HG") || (pair == "GH") ||(pair == "WT") ||(pair == "TW")){
            // add values of OPT for the line before t, for the line after t, and also add 1 to account for a[t] itself
            // NOTE: Because this iterative algorithm is bottom up, and thread-safe,
            // both of the table look-ups below should have memoized values already
            int opt = (opt_pairs_table[i][t-1]) + (opt_pairs_table[t+1][j-1]) + 1;
            // if the optimal number of pairs for this choice of t is larger than max_opt, make it max_opt
            if (opt >= max_opt){
                max_opt = opt;
            }
        }
    }

    // Memoize this result so we don't have to recompute it again, then return it
    opt_pairs_table[i][j] = max_opt;
    return max_opt;
}

string get_line_from_file(string file_name, int n){
    ifstream infile(file_name.c_str());
    if (infile.good() == 0){
        cout << "ERROR: file_name, " << file_name << " doesn't exist." << endl;
        return "";
    }
    string line;
    getline(infile, line);
    return line.substr(0, n);
}

int find_optimal_num_pairs_for_line(int n){
    // Initialize the line representation, a, which is a string on the alphabet, {H, G, W, T}
    a = get_line_from_file("test_data.txt", n);

    // Initialize a n-by-n 2D array of -1s, for storing memoized outputs of OPT for all i and j pairs
    vector<vector<int> > mat(n, vector<int>(n, -1));
    opt_pairs_table = mat;

    // Set the lower triangular region of opt_pairs_table to 0
    for (int row = 0; row < a.size(); row++){
        for (int col = 0; col < a.size() - row; col++){
            opt_pairs_table[col+row][col] = 0;
        }
    }

    // Calculate the optimal pairs for the line, and time the operation
    double start_time = omp_get_wtime();
    for (int col = 0; col < a.size(); col++){
        #pragma omp parallel for
        for (int row = 0; row < a.size() - col; row++){
            OPT(row, row+col);
        }
    }
    double time = omp_get_wtime() - start_time;

    cout << "n = " << n << ", OPT(1, n) = " << opt_pairs_table[0][n-1] << " (Done in " << time << " seconds)" << endl;

    return opt_pairs_table[0][n-1];
}

int main(){
    for (int n = 50; n < 1000; n+=50){
        find_optimal_num_pairs_for_line(n);
    }
    for (int n = 1000; n <= 2000; n+=200){
        find_optimal_num_pairs_for_line(n);
    }
}
