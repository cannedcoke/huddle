// first ill generate a laberinth
// show it
// meke it have 2 possible paths
// show it
// make then ill add obstacles via keyboard
// find the shortest path via a*


//importo mis librerias
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <deque>
#include <cstdlib>

using namespace std;


//defino mis constantes
const int DX[4] = {-1, 1, 0, 0};
const int DY[4] = {0, 0, 1, -1};
const int WALL = 1;
const int EMPTY = 0;
const int BUILDING = 2;
const int WATER = 3;
const int BLOCK = 4;
const int PATH = 7;


//genero un numero random para generar el laberinto
mt19937 rng(random_device{}());


// funcion para imprimir
void print(vector<vector<int>> &maze, int height, int width)
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
            if (maze[i][j] == 1)
            {
                cout << "\033[37m" << "██";
            }
            else if (maze[i][j] == 0)
            {
                cout << "  ";
            }
            else if (maze[i][j] == 2)
            {
                cout << "\033[30m" << "██" << "\033[37m";
            }
            else if (maze[i][j] == 3)
            {
                cout << "\033[34m" << "██" << "\033[37m";
            }
            else if (maze[i][j] == 4)
            {
                cout << "\033[31m" << "██" << "\033[37m";
            }
            else if (maze[i][j] == 5)
            {
                cout << "🚩";
            }
            else if (maze[i][j] == 6)
            {
                cout << "🏁";
            }
            else if (maze[i][j] == 7)
            {
                cout << "\033[33m" << "██" << "\033[37m";
            }
        }

        cout << "\n";
    }
}
//se genera el laberinto random usando depth firts search
void dfs(vector<vector<int>> &maze, int height, int width, int x, int y)
{

    vector<int> dirs = {0, 1, 2, 3};

    shuffle(dirs.begin(), dirs.end(), rng);

    for (auto d : dirs)
    {
        int nx = x + DX[d] * 2;
        int ny = y + DY[d] * 2;
        if (nx < 0 || nx >= width || ny < 0 || ny >= height)
            continue;
        if (maze[ny][nx] != WALL)
            continue;
        maze[y + DY[d]][x + DX[d]] = EMPTY;
        maze[ny][nx] = EMPTY;

        dfs(maze, height, width, nx, ny);
    }
}

// esta funcion echa algunas paredes random para que haya mas de un camino 
void hydra(vector<vector<int>> &maze, int height, int width)
{

    for (int k = 0; k < 20; k++)
    {
        int x = rng() % width;
        int y = rng() % height;

        if (maze[y][x] != WALL)
            continue;
        int empty_neigbours = 0;
        for (int i = 0; i < 4; i++)
        {
            int nx = x + DX[i];
            int ny = y + DY[i];
            if (nx < 0 || nx >= width || ny < 0 || ny >= height)
                continue;
            if (maze[ny][nx] == 0)
                empty_neigbours++;
        }
        if (empty_neigbours == 2)//si tiene dos espacios a su alredesdor echa la pared
        {
            maze[y][x] = 0;
        }
    }
}
//funcion para ubicar obstaculos
void obstacles(vector<vector<int>> &maze, int height, int width)
{

    int x, y;
    int obstaculo;
    char coma;

    cout << "ingrese 1 para edificio, 2 para agua y 3 para zona bloqueada: ";
    cin >> obstaculo;

    cout << "ingrese cordenadas en x e y como x,y: ";
    cin >> x >> coma >> y;
    if (x >= 0 && x < width && y >= 0 && y < height && maze[y][x] != WALL)
    {
        if (obstaculo == 1)
        {
            maze[y][x] = 2;
        }
        else if (obstaculo == 2)
        {
            maze[y][x] = 3;
        }
        else if (obstaculo == 3)
        {
            maze[y][x] = 4;
        }
    }
}

//funciion p ara checkear que este adentro del laberinto y devuelve un booleano
bool inside(vector<vector<int>> maze, int width, int height, int x, int y)
{
    if (x >= 0 && x < width && y >= 0 && y < height && maze[y][x] != WALL)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// funcion que ubica las posiciones de inicio y meta si cumple con las 
bool start_goal(vector<vector<int>> &maze, int width, int height, int start_x, int start_y, int end_x, int end_y)
{

    if (inside(maze, width, height, start_x, start_y) && inside(maze, width, height, end_x, end_y))
    {
        maze[start_y][start_x] = 5;
        maze[end_y][end_x] = 6;
        return false;
    }
    else
    {
        cout << "coordenadas invalidas, intente de nuevo ";
        return true;
    }
}
// funcion para recorrer el laberinto 
void A_star(vector<vector<int>> &maze, int height, int width, int start_x, int start_y, int end_x, int end_y)
{
    vector<vector<int>> cost_begining(height, vector<int>(width, 1e9));
    vector<vector<int>> estimate(height, vector<int>(width, 1e9));
    vector<vector<pair<int, int>>> parent(height, vector<pair<int, int>>(width, {-1, -1}));

    auto heuristic = [&](int x, int y)
    {
        return abs(x - end_x) + abs(y - end_y);
    };

    deque<pair<int, int>> explore;

    cost_begining[start_y][start_x] = 0;
    estimate[start_y][start_x] = heuristic(start_x, start_y);

    explore.push_back({start_x, start_y});

    while (!explore.empty())
    {
        int lowest_cost = 0;
        for (size_t i = 1; i < explore.size(); i++)
        {
            int x1 = explore[i].first;
            int y1 = explore[i].second;
            int x2 = explore[lowest_cost].first;
            int y2 = explore[lowest_cost].second;

            if (estimate[y1][x1] < estimate[y2][x2])
            {
                lowest_cost = i;
            }
        }
        int cur_x = explore[lowest_cost].first;
        int cur_y = explore[lowest_cost].second;

        explore.erase(explore.begin() + lowest_cost);//esto es para que no vuelva a procesar el mismo nodo

        if (cur_x == end_x && cur_y == end_y)
        {
            break;
        }

        for (int i = 0; i < 4; i++)
        {
            int nx = cur_x + DX[i];
            int ny = cur_y + DY[i];

            if (!inside(maze, width, height, nx, ny))
                continue;
            if (maze[ny][nx] == BUILDING)
                continue;
            if (maze[ny][nx] == WATER)
                continue;
            if (maze[ny][nx] == BLOCK)
                continue;

            int new_cost = cost_begining[cur_y][cur_x] + 1;

            if (new_cost < cost_begining[ny][nx])
            {
                cost_begining[ny][nx] = new_cost;

                estimate[ny][nx] = new_cost + heuristic(nx, ny);

                parent[ny][nx] = {cur_x, cur_y};

                explore.push_back({nx, ny});
            }
        }
    }

    vector<pair<int, int>> path;
    int path_x = end_x;
    int path_y = end_y;

    while (!(path_x == start_x && path_y == start_y))
    {
        pair<int, int> previo = parent[path_y][path_x];

        if(previo.first == -1){
            cout<<"no hay otro camino ";
            break;
        }
        path.push_back({path_x, path_y});

        path_x = previo.first;
        path_y = previo.second;
    }
    reverse(path.begin(), path.end());

    for (auto [px, py] : path)
    {
        if (maze[py][px] == EMPTY)
            maze[py][px] = PATH;
        system("cls");
        print(maze, height, width);
    }
}

int main()
{
    int x = 1;
    int y = 1;
    int height, width;
    char opcion;
    int start_x, start_y;
    int end_x, end_y;
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

    vector<vector<int>> maze(height, vector<int>(width, 1));

    dfs(maze, height, width, x, y);
    hydra(maze, height, width);
    print(maze, height, width);

    while (valid)
    {
        cout << "ingrese coordenadas de entrada  como x,y: ";
        cin >> start_x >> coma >> start_y;

        cout << "ingrese coordenadas de salida  como x,y: ";
        cin >> end_x >> coma >> end_y;
        valid = start_goal(maze, width, height, start_x, start_y, end_x, end_y);
    }
    print(maze, height, width);

    // solve it

    A_star(maze, height, width, start_x, start_y, end_x, end_y);

    while (opcion != 'n' && opcion != 'N')
    {
        cout << "deasea añadir obstaculos ? ( s/n ): ";
        cin >> opcion;
        if (opcion == 's' || opcion == 'S')
        {

            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    if (maze[j][i] == 7)
                    {
                        maze[j][i] = EMPTY;
                    }
                }
            }

            obstacles(maze, height, width);
            print(maze, height, width);
        }
    }

    A_star(maze, height, width, start_x, start_y, end_x, end_y);

    return 0;
}