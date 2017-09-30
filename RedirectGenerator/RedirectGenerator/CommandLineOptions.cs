using CommandLine;

namespace RedirectGenerator
{
    public class CommandLineOptions
    {
        [Option('c', "content", Required = true, HelpText = "Path to content that needs to be redirected.")]
        public string ContentPath
        {
            get;
            set;
        }

        [Option('b', "baseurl", Required = true, HelpText = "Base URL for new redirection targets.")]
        public string BaseUrl
        {
            get;
            set;
        }

        [Option('t', "targetfolder", Required = true, HelpText = "Location where the redirection file should be placed.")]
        public string TargetFolder
        {
            get;
            set;
        }

        [Option('r', "repoRoot", Required = true, HelpText = "Repository root.")]
        public string RepoRoot
        {
            get;
            set;
        }

        [Option('d', "delete", Required = true, HelpText = "Choose whether to delete files that need to be redirected.")]
        public bool DeleteFiles
        {
            get;
            set;
        }
    }
}
