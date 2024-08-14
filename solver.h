/*! \file
 * \brief Contains functions for solving equations
 *
 * supports solving quadratic and linear equations
 */

static const double EPSILON    =  1e-9;
static const double NAN_DOUBLE = -1;
static const int    NAN_INT    = -1;

/************************************************************//**
 * @brief Struct contains parameters of answers of the solved equation
 ************************************************************/

struct QuadSolutions
{
    int    amount;          ///< amount of roots
    double first;           ///< first root
    double second;          ///< second root
    char*  arg;             ///< output argument
};

/************************************************************//**
 * @brief Struct contains coefficients
 ************************************************************/

struct Coefficients
{
    double a;           ///< coefficient
    double b;           ///< coefficient
    double c;           ///< coefficient
    char*  arg;         ///< input argument
};

/************************************************************//**
 * @brief  enums comparison outcomes (a \/ b)
 ************************************************************/

enum Comparison
{
    LESS  = -1,          ///< a < b
    EQUAL =  0,          ///< a = b
    MORE  =  1,          ///< a > b
};

/************************************************************//**
 * @brief Function compares two double numbers, with EPSILON (1e-6) accuracy
 *
 * @param[in] a first number
 * @param[in] b second number
 * @return EQUAL if a = b
 * @return MORE  if a > b
 * @return LESS  if a < b
 ************************************************************/

int Compare(const double a, const double b);

/************************************************************//**
 * @brief Solves quadratic equation (ax^2 + bx + c = 0)
 *
 * @param[in] a coefficient
 * @param[in] b coefficient
 * @param[in] c coefficient
 * @param[out] ans equation answer
 ************************************************************/

void QuadSolver(const double a, const double b, const double c, struct QuadSolutions* ans);   // solving equation

/************************************************************//**
 * @brief Solves linear equatiion (bx + c = 0)
 *
 * @param[in] b coefficient
 * @param[in] c coefficient
 * @param[out] ans equation answer
 ************************************************************/

void LinearSolver(const double b, const double c, struct QuadSolutions* ans);

/************************************************************//**
 * @brief Enums number of equation roots
 ************************************************************/

enum Roots
{
    UNDEFINED_ROOTS  = -2,       ///< equation has undefined amount of roots
    INF_ROOTS        = -1,       ///< equation has infinite amount of roots
    ZERO_ROOTS       =  0,       ///< equation has no roots
    ONE_ROOT         =  1,       ///< equation has one root
    TWO_ROOTS        =  2,       ///< equation has two different roots
};

/************************************************************//**
 * @brief Compares number with zero (EPSILON accuracy)
 *
 * @param[in] nmb number
 * @return 0 if nmb is close to zero
 * @return nmb if it is not close to zero
 ************************************************************/

double inline IsZero(double* nmb);
