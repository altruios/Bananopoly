class BUTTON:
    def __init__(self,upgrade):
        self.name=self.generate_name(upgrade);
        self.costs=self.generate_costs(upgrade);
        self.effect=upgrade;
        self.presses=0;
        self.scale=1.2;
        self.pressed=False;
        self.singleUse=True;
    def generate_name(self,upgrade):
        name = 'upgrade:'
        print("upgrade targets",len(upgrade.targets))
        for t in upgrade.targets:
            print(t.name,"is t");
            name=name + " "+t.name+" "
        print(name,"is name");
        return name;
    def generate_costs(self,upgrade):
        costs=[];
        for building in upgrade.targets:
            for cost in building.costs:
                costs.append(costs);
        real_costs = [];
        for cost in costs:
            found = False;
            for c in real_costs:
                if c.name==cost.name: 
                    c.amount=c.amount+cost.amount;
                    found=True;
            if not found: real_costs.append(cost);
        return real_costs

    def update_costs(self):
        self.presses=self.presses+1;
        for c in self.costs:
            c=c+(self.presses*self.scale);
    def press(self,wallet):
        tests=[];
        for cost in self.costs:
            print(cost[0][0])
            for resource in wallet.resources:
                print(resource.name)
                print(cost.name);
                if(resource.name!=cost.name):continue;
                if(resource.amount-cost.amount>=0): tests.append(True)
                else: tests.append(False)    
        if not all(x for x in tests): return False;
        self.effect.apply();
        self.pressed=True;
        return True;