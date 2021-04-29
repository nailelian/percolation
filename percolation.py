import numpy as np
import matplotlib.pyplot as plt

class Percolation(object):
    def __init__(self, lattice):
        self.lattice = lattice
        self.n = self.lattice.shape[0]

        self.init_lat = lattice

    def reset(self):
        self.lattice = self.init_lat

    def update_lattice(self, i, j, val):
        self.lattice[i][j] = val

    def is_path_rec(self, row, col, visited):
        # check for success
        if col == self.n-1: return True, visited

        # check if already visited
        if visited[row][col] == 1:
            return False, visited
        else:
            visited[row][col] = 1

        # check for neighbours
        if row - 1 > 0 and self.lattice[row-1][col] == 1:
            success, visited = self.is_path_rec(row-1, col, visited)
            if success: return True, visited
        if row + 1 < self.n and self.lattice[row+1][col] == 1:
            success, visited = self.is_path_rec(row+1, col, visited)
            if success: return True, visited
        if col - 1 > 0 and self.lattice[row][col-1] == 1:
            success, visited = self.is_path_rec(row, col-1, visited)
            if success: return True, visited
        if col + 1 < self.n and self.lattice[row][col+1] == 1:
            success, visited = self.is_path_rec(row, col+1, visited)
            if success: return True, visited

        # return False if no success
        return False, visited

    def is_path(self):
        visited = np.zeros((self.n, self.n))

        for i in range(0, self.n):
            if self.lattice[i][0] == 1:
                success, visited = self.is_path_rec(i, 0, visited)
                if success: return True

        return False

    def percolate(self, p):
        self.reset()
        for i in range(0,self.n):
            for j in range(0,self.n):
                self.update_lattice(i,j,np.random.binomial(1, p))
        return self.lattice

    def simulate(self, iter, p):
        self.reset()
        n_True = 0
        for i in range(iter):
            self.reset()
            self.percolate(p)
            if self.is_path():
                n_True += 1
        return n_True / iter

#    def is_centre_path_rec(self):

    def is_centre_path(self):
        if self.n % 2 == 0: return None


class TriPercolation(Percolation):
    def is_path_rec(self, row, col, visited):
        # check for success
        if col == self.n-1: return True, visited

        # check if already visited
        if visited[row][col] == 1:
            return False, visited
        else:
            visited[row][col] = 1

        # check for neighbours
        if row - 1 > 0 and self.lattice[row-1][col] == 1:
            success, visited = self.is_path_rec(row-1, col, visited)
            if success: return True, visited
        if row + 1 < self.n and self.lattice[row+1][col] == 1:
            success, visited = self.is_path_rec(row+1, col, visited)
            if success: return True, visited
        if col - 1 > 0 and self.lattice[row][col-1] == 1:
            success, visited = self.is_path_rec(row, col-1, visited)
            if success: return True, visited
        if col + 1< self.n and self.lattice[row][col+1] == 1:
            success, visited = self.is_path_rec(row, col+1, visited)
            if success: return True, visited
        if col + 1 < self.n and row + 1 < self.n and self.lattice[row+1][col+1] == 1:
            success, visited = self.is_path_rec(row+1, col+1, visited)
            if success: return True, visited
        if col - 1 > 0 and row - 1 > 0 and self.lattice[row-1][col-1] == 1:
            success, visited = self.is_path_rec(row-1, col-1, visited)
            if success: return True, visited

        # return False if no success
        return False, visited

class PercolationSophisticated(Percolation):
    def percolate_rand(self, p):
        self.reset()
        for i in range(0,self.n):
            for j in range(0,self.n):
                self.update_lattice(i,j,random())
                if self.lattice[i][j] < p:
                    self.lattice[i][j] = 1
                else:
                    self.lattice[i][j] = 0
        return self.lattice

    #def find_critical_value():


class PercolationTools(object):
    def __init__(self, perc_obj):
        self.perc_obj = perc_obj

    def update_perc(self, perc_obj):
        self.perc_obj = perc_obj

    def display(self, ax, no_print=True):
        xi = np.arange(0, self.perc_obj.n+1)
        yi = np.arange(0, self.perc_obj.n+1)
        X, Y = np.meshgrid(xi, yi)

        # flipping array so output matches array
        if not no_print: print(self.perc_obj.lattice)
        ax.pcolormesh(X, Y, np.flipud(self.perc_obj.lattice))

    def find_critical_value_g(self, iter, dp):
        plt.figure()
        m = 10**dp
        xs = []
        ys = []
        for i in range(0, m):
            r = self.perc_obj.simulate(iter, i/m)
            xs.append(i/m)
            ys.append(r)
        plt.plot(xs, ys, "-bo")
        plt.show()

    def find_critical_value_bs(self, iter_sim, iter_search, l=0, u=1, m=0):
        p = (u+l)/2

        if m >= iter_search: return p

        r = self.perc_obj.simulate(iter_sim, p)

        print(l,p,u,r)

        if r < 0.5:
            return self.find_critical_value_bs(iter_sim, iter_search, p, u, m+1)
        else:
            return self.find_critical_value_bs(iter_sim, iter_search, l, p, m+1)

#fig, ax = plt.subplots()

#testing rafael
#test anna

#P = Percolation(np.zeros((10,10)))
#P.percolate(0.5)
#PT = PercolationTools(P)
#PT.display(ax)

#plt.show()

#PT.find_critical_value_g(50, 1)
