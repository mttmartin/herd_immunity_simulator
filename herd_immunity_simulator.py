#!/usr/bin/env python3
# A very simple epidemic simulation
import random

class World:
    def __init__(self):
        self.world_size=20
        self.people = list()
        self.population=0
        self.immune_num=0
        self.infected_num=0

    def add_person(self,person):
        self.people.append(person)
        self.population += 1

    def remove_person(self,person):
        self.people.remove(person)
        self.population -= 1

    def do_interactions(self):
        for i in range(len(self.people)):
            for j in range(len(self.people)):
                if i == j:
                    continue
                if self.people[i].get_loc() == self.people[j].get_loc():
                    self.people[i].interact(self.people[j])
                    self.people[j].interact(self.people[i])

    def immunize_population(self,percent,vaccine):
        num_to_vaccinate = int(self.get_population() * percent/100.0)

        for i in range(num_to_vaccinate):
           self.people[i].vaccinate(vaccine)

    def tick(self):
        infected_num=0
        immune_num=0
        for person in self.people:
            person.tick()
            if person.is_infected():
                infected_num += 1
            if person.is_immune():
                immune_num += 1
            person.set_pos(random.randint(0,self.world_size),random.randint(0,self.world_size))
            if person.get_alive() == False:
                self.remove_person(person)
        self.do_interactions()
        self.infected_num = infected_num
        self.immune_num = immune_num

    def get_infected(self):
        return self.infected_num

    def get_immune(self):
        return self.immune_num

    def get_population(self):
        return self.population

class Pathogen:
    def __init__(self,score=0.1,infect_time=5,lethality=0.5):
        self.score = score
        self.infect_time = infect_time
        self.lethality = lethality

    def get_score(self):
        return self.score

    def get_infect_time(self):
        return self.infect_time

    def get_lethality(self):
        return self.lethality

class Person:
    def __init__(self):
        self.immune = False
        self.alive = True
        self.infected = False
        self.vaccinated = False
        self.vaccine_effect = 0
        self.infect_time = 0
        self.pathogen = None
        self.x = random.randint(0,50)
    def exposure(self,pathogen):
        if self.immune:
            return

        if random.random()+self.vaccine_effect < pathogen.get_score():
            self.infected = True
            self.infect_time = 0
            self.pathogen=pathogen

    def tick(self):
        if self.infected:
            self.infect_time += 1
            if self.infect_time > self.pathogen.get_infect_time():
                if random.random() < self.pathogen.get_lethality():
                    self.alive = False
                self.pathogen = None
                self.immune = True
                self.infected = False

    def vaccinate(self,vaccine):
        self.vaccinated = True
        self.vaccine_effect = vaccine.get_effect_score()

    def get_vaccinated(self):
        return self.vaccinated

    def set_pos(self,x,y):
        self.x = x
        self.y = y

    def get_loc(self):
        return self.x,self.y

    def is_infected(self):
        return self.infected

    def interact(self,other):
        if self.is_infected():
            return
        if other.is_infected():
            self.exposure(other.get_pathogen())

    def get_pathogen(self):
        return self.pathogen

    def infect(self,pathogen):
        self.infected=True
        self.infect_time = 0
        self.pathogen = pathogen

    def get_alive(self):
        return self.alive

    def is_immune(self):
        return self.immune

class Vaccine:
    def __init__(self,effect_score=0.95):
        self.effect_score = effect_score

    def get_effect_score(self):
        return self.effect_score

def main():
    pathogen = Pathogen(score=0.6,lethality=0.05)
    pop_target=100

    world = World()
    for i in range(pop_target):
        person = Person()
        if i == 0:
            person.infect(pathogen)
        world.add_person(person)

    vac1 = Vaccine(effect_score=0.80)
    world.immunize_population(60,vac1)

    target_tick = 50
    for i in range(target_tick):
        world.tick()
        infected_num = world.get_infected()
        immune_num = world.get_immune()
        total_pop = world.get_population()
        not_infected_num = total_pop - infected_num

        print("Tick:        \t", i)
        print("Infected:    \t", infected_num)
        print("Not infected:\t", not_infected_num)
        print("Immune:      \t", immune_num)
        print("\n")

if __name__ == "__main__":
    main()
