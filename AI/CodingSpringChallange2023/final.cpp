#include <iostream>
#include <algorithm>
#include <cmath>
#include <map>
#include <list>
#include <queue>
#include <vector>

using namespace std;

class Cell {
public:
    int idx, cellType, resources, pAnts, oppAnts;
    array<int, 6> neighbors{-1, -1, -1, -1, -1, -1};

    Cell() = default;

    void set(int idx, int cellType, int resources, array<int, 6> neighbors, int pAnts = 0, int oppAnts = 0) {
        this->idx = idx;
        this->cellType = cellType;
        this->resources = resources;
        this->neighbors = neighbors;
        this->pAnts = pAnts;
        this->oppAnts = oppAnts;
    }

    void update(int resources, int pAnts, int oppAnts) {
        this->resources = resources;
        this->pAnts = pAnts;
        this->oppAnts = oppAnts;
    }
};

int main() {
    int totalCrystals = 0, totalEggs = 0;
    int noCrystalsCells = 0, noCells = 0;
    cin >> noCells; cin.ignore();
    vector<Cell> cells(noCells);
    vector<int> cellNeighborsCost(noCells);
    vector<int> cellCost(noCells, -1);
    vector<int> pResources;
    vector<int> pEggs;
    vector<int> pCrystals;

    for (int i = 0; i < noCells; i++) {
        int type, initialResources;
        int neigh0, neigh1, neigh2, neigh3, neigh4, neigh5;
        cin >> type >> initialResources >> neigh0 >> neigh1 >> neigh2 >> neigh3 >> neigh4 >> neigh5; cin.ignore();

        cells[i].set(i, type, initialResources, {neigh0, neigh1, neigh2, neigh3, neigh4, neigh5}, 0, 0);
        if (type == 1) {
            totalEggs += initialResources;
            pEggs.push_back(i);
        }
        else if (type == 2) {
            totalCrystals += initialResources;
            noCrystalsCells++;
            pCrystals.push_back(i);
        }
        else {
            pResources.push_back(i);
        }

        cellCost[i] = initialResources;
    }

    for (auto c : cells) {
        for (auto n : c.neighbors) {
            if (n != -1)
                cellNeighborsCost[c.idx] += cells[n].resources;
        }
    }

    list<int> toVisit;
    vector<int> distanceToBase(noCells, -1);
    vector<int> previousNeighbour(noCells, -1);
    vector<int> closestBase(noCells, -1);

    int noBases;
    cin >> noBases; cin.ignore();

    vector<int> pBases, oppBases;
    for (int i = 0; i < noBases; i++) {
        int pBaseIdx;
        cin >> pBaseIdx; cin.ignore();
        pBases.push_back(pBaseIdx);
        toVisit.push_back(pBaseIdx);
        distanceToBase[pBaseIdx] = 0;
        previousNeighbour[pBaseIdx] = pBaseIdx;
        closestBase[pBaseIdx] = pBaseIdx;
    }

    for (int i = 0; i < noBases; i++) {
        int oppBaseIdx;
        cin >> oppBaseIdx; cin.ignore();
        oppBases.push_back(oppBaseIdx);
    }

    while (!toVisit.empty()) {
        auto current = toVisit.front();
        toVisit.pop_front();
        for (const auto& c : cells[current].neighbors) {
            if (c == -1 || find(pBases.cbegin(), pBases.cend(), c) != pBases.cend())
                continue;

            int newCost = cells[c].resources + (cellNeighborsCost[c] / (distanceToBase[current] + 2));

            if (distanceToBase[c] == -1 || newCost > cellCost[c] ||
                (newCost == cellCost[c] && distanceToBase[c] > distanceToBase[current] + 1)) {
                cellCost[c] = newCost;
                distanceToBase[c] = distanceToBase[current] + 1;
                previousNeighbour[c] = current;
                closestBase[c] = closestBase[current];
                toVisit.remove(c);
                toVisit.insert(find_if(toVisit.begin(), toVisit.end(), [c, &cellCost]
                (auto e) {return cellCost[c] > cellCost[e];}), c);
            }
        }
    }

    sort(pEggs.begin(), pEggs.end(), [&cells, &distanceToBase](auto e1, auto e2) {
        if (distanceToBase[e1] == distanceToBase[e2])
            return cells[e1].resources > cells[e2].resources;
        return distanceToBase[e1] < distanceToBase[e2];
        });

    sort(pCrystals.begin(), pCrystals.end(), [&cells, &distanceToBase](auto c1, auto c2) {
        if (distanceToBase[c1] == distanceToBase[c2])
            return cells[c1].resources > cells[c2].resources;
        return distanceToBase[c1] < distanceToBase[c2];
        });

    sort(pResources.begin(), pResources.end(), [&cells, &distanceToBase, &cellCost](auto r1, auto r2) {
        if (cells[r1].resources == cells[r2].resources)
            return cellCost[r1] > cellCost[r2];
        return cells[r1].resources > cells[r2].resources;
        });

    // game loop
    while (true) {
        int pScore, oppScore;
        cin >> pScore >> oppScore; cin.ignore();
        int availableCrystals = 0, availableEggs = 0, availableAnts = 0, oppAvailableAnts = 0;
        for (int i = 0; i < noCells; i++) {
            int resources, pAnts, oppAnts;
            cin >> resources >> pAnts >> oppAnts; cin.ignore();
            cells[i].update(resources, pAnts, oppAnts);
            availableAnts += pAnts;
            oppAvailableAnts += oppAnts;

            if (cells[i].cellType == 1)
                availableEggs += resources;
            else if (cells[i].cellType == 2)
                availableCrystals += resources;
        }

        int remainingAnts = availableAnts;
        int close = log(noCells);
        // cerr << "remaining ANTS " << remainingAnts << endl;
        // Collect eggs
        for (const auto& e : pEggs) {
            if (distanceToBase[e] <= close && cells[e].resources > 0) {
                int s = close - distanceToBase[e] + 1;
                if (availableEggs >= totalEggs / 2)
                    s += 1;
                cout << "LINE " << e << " " << closestBase[e] << " " << s << ";";
                if (cells[previousNeighbour[e]].pAnts)
                    remainingAnts--;
                else
                    remainingAnts -= distanceToBase[e];
            }
        }
        // cerr << "remaining ANTS after eggs " << remainingAnts << endl;

        // Prioritize collecting crystals
        for (const auto& c : pCrystals) {
            if (distanceToBase[c] <= close && cells[c].resources > 0) {
                int s = close - distanceToBase[c] + 1;
                int numAnts = min(cells[c].resources, remainingAnts);
                cout << "LINE " << c << " " << closestBase[c] << " " << s << ";";
                if (cells[previousNeighbour[c]].pAnts)
                    remainingAnts--;
                else
                    remainingAnts -= distanceToBase[c];
            }
        }
        // cerr << "remaining ANTS after crystals " << remainingAnts << endl;

        // Collect other resources
        for (const auto& r : pResources) {
            cerr << "Distance to base " << distanceToBase[r] << endl;
            if (distanceToBase[r] <= remainingAnts) {
                int idx = r, s = 1;
                while (idx != closestBase[r]) {
                    if (distanceToBase[idx] <= close || cells[idx].resources > 0)
                        s = 2;
                    cout << "LINE " << idx << " " << previousNeighbour[idx] << " " << s << ";";
                    idx = previousNeighbour[idx];
                }
                if (cells[previousNeighbour[r]].pAnts)
                    remainingAnts--;
                else
                    remainingAnts -= distanceToBase[r];
            }
        }
        // cerr << "remaining ANTS after other " << remainingAnts;

        cout << endl;
    }
}