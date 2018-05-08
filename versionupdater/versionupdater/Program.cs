using CommandLine;
using Csv;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using versionupdater.Models;

namespace versionupdater
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Version Updater 1.0");
            if (args.Any())
            {
                foreach (string arg in args)
                {
                    Console.WriteLine(arg);
                }
            }

            Parser.Default.ParseArguments<CommandLineOptions>(args).WithParsed(options =>
            {
                if (!string.IsNullOrWhiteSpace(options.CsvPath))
                {
                    StringBuilder builder = new StringBuilder();
                    using (FileStream stream = new FileStream(options.CsvPath, FileMode.Open))
                    {
                        Console.WriteLine("File opened...");
                        CsvOptions csvOptions = new CsvOptions();
                        csvOptions.HeaderMode = HeaderMode.HeaderAbsent;

                        var csvFile = CsvReader.ReadFromStream(stream, csvOptions);

                        var csvLines = csvFile.ToList();
                        Console.WriteLine($"Lines in file: {csvLines.Count()}");

                        Task.Run(async () =>
                        {
                            foreach (var line in csvLines)
                            {
                                Console.WriteLine("Processing CSV entry...");

                                var packageId = line[1];
                                packageId = Regex.Replace(packageId, @"(\[(.*?)\])*", "");

                                Console.WriteLine($"Package ID: {packageId}");
                                HttpClient client = new HttpClient();
                                var response =
                                    await client.GetAsync(
                                        $"https://api.nuget.org/v3/registration3/{packageId.ToLower()}/index.json");
                                var contents = await response.Content.ReadAsStringAsync();

                                try
                                {
                                    JObject jsonContent = JObject.Parse(contents);
                                    var deserializedContent = JsonConvert.DeserializeObject<NuGetPackage>(jsonContent.ToString());

                                    var version = (from c in deserializedContent.items.Last().items where c.catalogEntry.listed == true select c).Last().catalogEntry.version;

                                    Console.WriteLine(packageId);

                                    if (packageId.Equals("Microsoft.ServiceFabric.Data", StringComparison.InvariantCultureIgnoreCase))
                                    {
                                        Console.WriteLine("Here it is!");
                                    }
                                    Console.WriteLine("Latest version: " + version);

                                    builder.AppendLine($"{line[0]},{line[1]},{version}");
                                }
                                catch
                                {
                                    Console.WriteLine("Could not get information for package: " + packageId);
                                }
                            }
                        }).Wait();
                    }

                    File.WriteAllText(options.CsvPath, builder.ToString());
                }
            });
        }
    }
}
