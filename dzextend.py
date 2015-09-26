    def GetIndexPlugin(self,target):
        respone=self.Request_Get(target)
        plugin_finds=[]
        plugin=r'<a href="plugin.php\?id=(.*?)" hidefocus="true"'
        plugin=[r'plugin.php\?id=(.*)\&',r'src="plugin.php\?id=(.*)"','href="plugin.php\?id=(.*)"']
        for p in plugin:
            plugin_find=re.findall(p,respone)
            for p in plugin_find:
                if ':' in p:
                    p=p.split(":")[0]
                plugin_finds.append(p)
        return set(plugin_finds)
