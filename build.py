from cpt.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=False)
    if platform.system() == "Linux":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if settings["arch"] == 'x86':
                continue
            if settings["build_type"] != 'Release':
                continue

            new_settings = settings.copy()
            if settings["compiler.libcxx"] == "libstdc++":
                if settings["compiler"] == "clang":
                    new_settings["compiler.libcxx"] = "libstdc++11"
            filtered_builds.append([new_settings, options, env_vars, build_requires])
        builder.builds = filtered_builds
    builder.run()
