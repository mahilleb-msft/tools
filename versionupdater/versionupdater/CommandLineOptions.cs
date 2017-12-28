using CommandLine;
using System;
using System.Collections.Generic;
using System.Text;

namespace versionupdater
{
    internal class CommandLineOptions
    {
        [Option('c', "csv", Required = true, HelpText = "Path to the CSV file.")]
        public string CsvPath { get; set; }
    }
}
