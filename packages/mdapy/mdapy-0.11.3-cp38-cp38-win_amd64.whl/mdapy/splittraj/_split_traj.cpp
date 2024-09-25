#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>

namespace py = pybind11;
namespace fs = std::filesystem;

void split_xyz(const std::string &input_file, const std::string &outputdir = "res", const std::string &output_file_prefix = "")
{
    // Create the output directory if it doesn't exist
    fs::create_directories(outputdir);

    std::string prefix = output_file_prefix;
    if (prefix.empty())
    {
        size_t last_dot = input_file.find_last_of(".");
        if (last_dot != std::string::npos)
        {
            prefix = input_file.substr(0, last_dot);
        }
        else
        {
            prefix = input_file;
        }
    }

    std::ifstream infile(input_file);
    if (!infile.is_open())
    {
        std::cerr << "Failed to open the input file: " << input_file << std::endl;
        return;
    }

    int frame = 0;
    while (true)
    {
        std::string line;
        std::getline(infile, line);
        if (infile.eof())
            break;

        std::cout << "\rSaving frame " << frame << std::flush;
        int n = std::stoi(line);

        std::string output_file = outputdir + "/" + prefix + "." + std::to_string(frame) + ".xyz";
        std::ofstream outfile(output_file);
        if (!outfile.is_open())
        {
            std::cerr << "Failed to open the output file: " << output_file << std::endl;
            return;
        }

        outfile << line << "\n";
        for (int i = 0; i <= n; ++i)
        {
            std::getline(infile, line);
            outfile << line << "\n";
        }
        outfile.close();
        ++frame;
    }
    infile.close();
    std::cout << std::endl;
}

PYBIND11_MODULE(_split_traj, m)
{
    m.def("split_xyz", &split_xyz);
}
