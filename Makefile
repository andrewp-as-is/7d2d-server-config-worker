all:
	rm -fr base_apps

	# git clone git@github.com:andrewp-as-is/python42.com-base.git base
	cp -R ~/git/7d2d.com-base-apps/ base_apps

	find . -type d -name .git -mindepth 2 -exec rm -fr {} \; ;:
