#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <deque>
#include <cstdlib>

using namespace std;

const int DX[4] = {-1, 1, 0, 0};
const int DY[4] = {0, 0, 1, -1};

enum class Cell
{

    wall,
    empty,
    building,
    water,
    block,
    path,
    start,
    end
};

// genero un numero random para generar el laberinto
mt19937 rng(random_device{}());

// creo mi clase para imprimir

class Maze
{
private:
    int height;
    int width;
    vector<vector<Cell>> grid;

public:
    int getHeight() const { return height; }
    int getWidth() const { return width; }
    const vector<vector<Cell>> &getGrid() const { return grid; }
    Maze(int h, int w) : height(h), width(w), grid(h, vector<Cell>(w, Cell::wall)) {}

    void clear()
    {
        // Clear previous path marks
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                if (grid[i][j] == Cell::path)
                {
                    grid[i][j] = Cell::empty;
                }
            }
        }
    }

    bool inside(int x, int y) const
    {
        return x >= 0 && x < width && y >= 0 && y < height;
    };

    bool isWalkable(int x, int y) const
    {
        if (!inside(x, y))
            return false;

        Cell cell = grid[y][x];

        return cell != Cell::wall;
    };

    void print()
    {
        // imprime los numeros para saber la poscicion
        cout << "    ";
        for (int j = 0; j < width; j++)
        {
            if (j < 10)
                cout << j << " ";
            else
                cout << j; // adjust spacing for >9
        }
        cout << "\n";

        // se imprime el laberinto con sus diferentes cosas
        for (int i = 0; i < height; i++)
        {

            if (i < 10)
                cout << i << "   ";
            else
                cout << i << "  ";

            for (int j = 0; j < width; j++)
            {
                if (grid[i][j] == Cell::wall)
                    cout << "\033[37m" << "██";

                else if (grid[i][j] == Cell::empty)
                    cout << "  ";

                else if (grid[i][j] == Cell::building)
                    cout << "\033[30m" << "██" << "\033[37m";

                else if (grid[i][j] == Cell::water)
                    cout << "\033[34m" << "██" << "\033[37m";

                else if (grid[i][j] == Cell::block)
                    cout << "\033[31m" << "██" << "\033[37m";

                else if (grid[i][j] == Cell::start)
                    cout << "🚩";

                else if (grid[i][j] == Cell::end)
                    cout << "🏁";

                else if (grid[i][j] == Cell::path)
                    cout << "\033[33m" << "██" << "\033[37m";
            }

            cout << "\n";
        }
    };

    void dfs(int x, int y)
    {
        deque<int> dirs = {0, 1, 2, 3};

        shuffle(dirs.begin(), dirs.end(), rng);

        for (auto d : dirs)
        {
            int nx = x + DX[d] * 2;
            int ny = y + DY[d] * 2;
            // if (!inside(maze,width,height,nx,ny))continue;
            if (!inside(nx, ny))
                continue;
            if (grid[ny][nx] != Cell::wall)
                continue;

            grid[y + DY[d]][x + DX[d]] = Cell::empty;
            grid[ny][nx] = Cell::empty;

            dfs(nx, ny);
        }
    };
    // esta funcion echa algunas paredes random para que haya mas de un camino
    // actually kinda dodgy but works
    void hydra()
    {

        for (int k = 0; k < height; k++)
        {
            int x = rng() % width;
            int y = rng() % height;

            if (grid[y][x] != Cell::wall)
                continue;
            int empty_neigbours = 0;
            for (int i = 0; i < 4; i++)
            {
                int nx = x + DX[i];
                int ny = y + DY[i];
                if (nx < 0 || nx >= width || ny < 0 || ny >= height)
                    continue;
                if (grid[ny][nx] == Cell::empty)
                    empty_neigbours++;
            }
            if (empty_neigbours == 2) // si tiene dos espacios a su alredesdor echa la pared
            {
                grid[y][x] = Cell::empty;
            }
        }
    };

    // funcion para ubicar obstaculos
    void obstacles()
    {

        int x, y;
        int obstaculo;
        char coma;

        cout << "ingrese 1 para edificio, 2 para agua y 3 para zona bloqueada: ";
        cin >> obstaculo;

        cout << "ingrese cordenadas en x e y como x,y: ";
        cin >> x >> coma >> y;
        if (inside(x, y) && isWalkable(x, y))
        {
            if (obstaculo == 1)
            {
                grid[y][x] = Cell::building;
            }
            else if (obstaculo == 2)
            {
                grid[y][x] = Cell::water;
            }
            else if (obstaculo == 3)
            {
                grid[y][x] = Cell::block;
            }
        }
    }

    // funcion que ubica las posiciones de inicio y meta si cumple con las condiciones
    bool start_goal(int start_x, int start_y, int end_x, int end_y)
    {

        if (inside(start_x, start_y) && inside(end_x, end_y) && isWalkable(start_x, start_y) && isWalkable(end_x, end_y))
        {
            grid[start_y][start_x] = Cell::start;
            grid[end_y][end_x] = Cell::end;
            return false;
        }
        else
        {
            cout << "coordenadas invalidas, intente de nuevo ";
            return true;
        }
    }

    void A_star(int start_x, int start_y, int end_x, int end_y)
    {

        vector<vector<int>> g_cost(height, vector<int>(width, 1e9));
        vector<vector<int>> f_cost(height, vector<int>(width, 1e9));
        vector<vector<pair<int, int>>> parent(height, vector<pair<int, int>>(width, {-1, -1}));

        auto heuristic = [&](int x, int y)
        {
            return abs(x - end_x) + abs(y - end_y);
        };

        g_cost[start_y][start_x] = 0;
        f_cost[start_y][start_x] = heuristic(start_x, start_y);
        vector<pair<int, int>> open_list;
        open_list.push_back({start_x, start_y});

        while (!open_list.empty())
        {
            int best_index = 0;
            for (size_t i = 1; i < open_list.size(); i++)
            {
                int x = open_list[i].first;
                int y = open_list[i].second;
                int best_x = open_list[best_index].first;
                int best_y = open_list[best_index].second;
                if (f_cost[y][x] < f_cost[best_y][best_x])
                {
                    best_index = i;
                }
            }

            int current_x = open_list[best_index].first;
            int current_y = open_list[best_index].second;

            open_list.erase(open_list.begin() + best_index);

            if (current_x == end_x && current_y == end_y)
            {
                break;
            }
            int tentative;
            for (int i = 0; i < 4; i++)
            {
                int new_x = current_x + DX[i];
                int new_y = current_y + DY[i];

                if (!inside(new_x, new_y))
                    continue;
                if (grid[new_y][new_x] == Cell::building)
                    continue;
                if (grid[new_y][new_x] == Cell::block)
                    continue;
                if (grid[new_y][new_x] == Cell::wall)
                    continue;
                if (grid[new_y][new_x] == Cell::water)
                {
                    tentative = g_cost[current_y][current_x] + 2;
                }
                else
                {
                    tentative = g_cost[current_y][current_x] + 1;
                }

                // int *puntero;
                // puntero = &tentative;

                if (tentative < g_cost[new_y][new_x])
                {
                    g_cost[new_y][new_x] = tentative;
                    f_cost[new_y][new_x] = heuristic(new_x, new_y) + tentative;
                    parent[new_y][new_x] = {current_x, current_y};

                    open_list.push_back({new_x, new_y});
                }
            }
        }

        // reconstruccion de camino
        vector<pair<int, int>> path;

        int path_x = end_x;
        int path_y = end_y;

        while (!(path_x == start_x && path_y == start_y))
        {
            pair<int, int> prev = parent[path_y][path_x];

            if (prev.first == -1)
            {
                cout << "no hay otro camino";
                break;
            }

            path.push_back({path_x, path_y});
            path_x = prev.first;
            path_y = prev.second;
        }

        reverse(path.begin(), path.end());

        for (auto [x, y] : path)
        {
            if (grid[y][x] == Cell::empty)
            {
                grid[y][x] = Cell::path;
            }
        }
        system("cls");
        print();
    }
};

int main()
{
    int x = 1;
    int y = 1;
    int height, width;
    char opcion;
    int start_x, start_y, end_x, end_y;
    char coma;
    bool valid = true;

    cout << " ingrese altura del laberinto: ";
    cin >> height;
    cout << " ingrese ancho del laberinto: ";
    cin >> width;

    if (height % 2 == 0)
        height++;
    if (width % 2 == 0)
        width++;

    // vector<vector<int>> maze(height, vector<int>(width, 1));
    Maze maze(height, width);

    maze.dfs(x, y);
    maze.hydra();
    maze.print();

    while (valid) // marcar coordenadas de entrada y salida en el laberinto
    {
        cout << "ingrese coordenadas de entrada  como x,y: ";
        cin >> start_x >> coma >> start_y;

        cout << "ingrese coordenadas de salida  como x,y: ";
        cin >> end_x >> coma >> end_y;
        valid = maze.start_goal(start_x, start_y, end_x, end_y);
    }
    maze.print();

    // solve it

    maze.A_star(start_x, start_y, end_x, end_y);

    do
    {
        cout << "Desea añadir obstaculos? (s/n): ";
        cin >> opcion;

        if (opcion == 's' || opcion == 'S')
        {
            maze.clear();
            maze.obstacles();
            maze.clear();
            maze.A_star(start_x, start_y, end_x, end_y);
            // maze.print();
        }

    } while (opcion != 'n' && opcion != 'N');
    cout << "gracias por jugar!";

    return 0;
}