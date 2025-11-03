local dap = require("dap")

dap.adapters.python = function(cb, config)
	cb({
		type = "executable",
		command = vim.fs.normalize("~/venvs/srcpool/bin/python3"),
		args = { "-m", "debugpy.adapter" },
		options = {
			source_filetype = "python",
		},
	})
end

local cwd = vim.fn.getcwd()

dap.configurations.python = {
	{
		-- The first three options are required by nvim-dap
		type = "python", -- the type here established the link to the adapter definition: `dap.adapters.python`
		request = "launch",
		name = "github-test",

		-- Options below are for debugpy, see https://github.com/microsoft/debugpy/wiki/Debug-configuration-settings for supported options

		program = vim.fs.normalize("~/venvs/srcpool/bin/srcpool"), -- This configuration will launch the current file if used.
		pythonPath = vim.fs.normalize("~/venvs/srcpool//bin/python3"),
		args = { "github", "RubixDev" },
	},
}
