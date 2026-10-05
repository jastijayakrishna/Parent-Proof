#!/bin/sh
# Installs the Parent verifier: the latest release's binary for this machine,
# checked against the release's SHA256SUMS. PARENT_INSTALL_DIR (default: the
# current directory) is where it goes.
#
#   curl -fsSL https://raw.githubusercontent.com/jastijayakrishna/Parent-Proof/main/install.sh | sh
set -eu
repo=${PARENT_REPO:-jastijayakrishna/Parent-Proof}
base=${PARENT_BASE_URL:-https://github.com/$repo/releases/latest/download}
dir=${PARENT_INSTALL_DIR:-.}
case $(uname -s) in
Linux) os=linux ;;
Darwin) os=darwin ;;
MINGW* | MSYS* | CYGWIN*) os=windows ;;
*)
	echo "install.sh: $(uname -s) is not supported; download a binary from https://github.com/$repo/releases" >&2
	exit 1
	;;
esac
case $(uname -m) in
x86_64 | amd64) arch=amd64 ;;
arm64 | aarch64) arch=arm64 ;;
*)
	echo "install.sh: $(uname -m) is not supported; download a binary from https://github.com/$repo/releases" >&2
	exit 1
	;;
esac
ext=
if [ "$os" = windows ]; then ext=.exe; fi
name=verifier-$os-$arch$ext
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
curl -fsSL -o "$tmp/$name" "$base/$name"
curl -fsSL -o "$tmp/SHA256SUMS" "$base/SHA256SUMS"
want=$(grep -E "[ *]$name\$" "$tmp/SHA256SUMS" | cut -d' ' -f1)
if command -v sha256sum >/dev/null 2>&1; then
	have=$(sha256sum "$tmp/$name" | cut -d' ' -f1)
else
	have=$(shasum -a 256 "$tmp/$name" | cut -d' ' -f1)
fi
if [ -z "$want" ] || [ "$want" != "$have" ]; then
	echo "install.sh: $name does not match the release's SHA256SUMS; nothing was installed" >&2
	exit 1
fi
mkdir -p "$dir"
mv "$tmp/$name" "$dir/verifier$ext"
chmod +x "$dir/verifier$ext"
"$dir/verifier$ext" version
echo "Installed $dir/verifier$ext. Start with: $dir/verifier$ext report --repo YOUR_PROTO_REPO --callers SERVICE_DIR[,SERVICE_DIR]"
