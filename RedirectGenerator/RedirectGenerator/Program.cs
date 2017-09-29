using CommandLine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;

namespace RedirectGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            ParserResult<CommandLineOptions> options = Parser.Default.ParseArguments<CommandLineOptions>(args);

            if (options != null)
            {
                options.WithParsed(t => ProcessData(t));
            }
        }

        static void ProcessData(CommandLineOptions options)
        {
            if (!string.IsNullOrWhiteSpace(options.ContentPath) && !string.IsNullOrWhiteSpace(options.BaseUrl)
                && !string.IsNullOrWhiteSpace(options.TargetFolder) && !string.IsNullOrWhiteSpace(options.RepoRoot))
            {
                RedirectionRoot root = new RedirectionRoot();
                
                var filesNeedingToBeRedirected = Directory.GetFiles(options.ContentPath);
                
                if (filesNeedingToBeRedirected != null)
                {
                    foreach(var file in filesNeedingToBeRedirected)
                    {
                        if (!Path.GetFileName(file).StartsWith(".") && !Path.GetFileName(file).StartsWith("toc.yml"))
                        {
                            root.RedirectionObjects.Add(new RedirectionObject()
                            {
                                SourcePath = file.Replace(options.RepoRoot, "").Replace(@"\\",@"\").Remove(0,1),
                                RedirectUrl = options.BaseUrl + "/" + Path.GetFileNameWithoutExtension(file),
                                RedirectDocumentId = true
                            });
                        }
                    }

                    var jsonString = JsonConvert.SerializeObject(root);

                    File.WriteAllText(Path.Combine(options.TargetFolder, ".openpublishing.redirection.json"), jsonString);
                    Console.WriteLine("Redirection file generation complete.");
                }
            }
        }
    }
}
